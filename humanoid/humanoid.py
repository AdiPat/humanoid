#
# Humanoid: A simple, natural language interface for orchestrating autonomous agents.
# File: humanoid.py
# Author: Aditya Patange (AdiPat)
# License: MIT License
#

import os
import copy
import traceback
from typing import Union, Any, List

from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from rich import print as rprint  # Add this import for rich printing
from rich.pretty import Pretty  # Add this import for pretty printing

from crewai import Agent, Task, Crew
from crewai.crew import CrewOutput

from .tooling import get_available_tools


class PreparedCrew(BaseModel):
    """Prepared crew model."""

    crew: Crew
    tasks: List[Task]
    input_data: dict


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    id: str
    role: str
    goal: str
    backstory: str
    allow_delegation: bool
    verbose: bool


class AgentReference(BaseModel):
    """Reference to an agent by ID."""

    id: str


class TaskConfig(BaseModel):
    """Configuration for a task."""

    description: str
    expected_output: str
    tools: list[str]
    agent: AgentReference


class CrewSettings(BaseModel):
    """Settings for the crew."""

    verbose: bool
    memory: bool


class InputConfig(BaseModel):
    """Configuration for input data."""

    key: str
    value: str


class CrewConfig(BaseModel):
    """Configuration for the entire crew."""

    crew: CrewSettings
    agents: list[AgentConfig]
    tasks: list[TaskConfig]
    input: list[InputConfig]


class GenerateCrewError(BaseModel):
    """Error model for crew generation."""

    error: str
    message: str


class Humanoid:
    """Main class for the Humanoid application."""

    def __init__(self):
        """Initialize the Humanoid instance."""
        rprint("🤖 [bold green]Initializing Humanoid...[/bold green]")
        init_result = self.init()
        if init_result.get("error"):
            raise Exception(
                init_result.get("message") + " - Error:" + init_result.get("error")
            )
        self.ai: OpenAI = init_result.get("openai_client", None)
        rprint("✅ [bold green]Humanoid initialized successfully![/bold green]")

    def init(self) -> dict:
        """Initializes the OpenAI API client."""
        try:
            rprint("🔧 [bold blue]Loading environment variables...[/bold blue]")
            load_dotenv(dotenv_path=".env", override=True)
            api_key = os.getenv("OPENAI_API_KEY")
            rprint("🔑 [bold blue]Initializing OpenAI API client...[/bold blue]")
            client = OpenAI(api_key=api_key)
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "This is a ping test. Respond with pong.",
                    },
                    {"role": "user", "content": "What's your response?"},
                ],
            )
            rprint(
                "✅ [bold green]OpenAI API client initialized successfully![/bold green]"
            )
            return {
                "message": "OpenAI API client initialized successfully.",
                "openai_client": client,
            }
        except Exception as e:
            rprint("❌ [bold red]Failed to initialize OpenAI API client![/bold red]")
            return {
                "error": str(e),
                "message": "An unexpected error occurred while initializing the OpenAI API client.",
            }

    def __prepare_crew_from_config(self, config: CrewConfig) -> PreparedCrew:
        """Prepares the crew using the specified config and input data."""
        rprint("🛠️ [bold blue]Preparing crew from config...[/bold blue]")
        agents_config = config.agents
        tasks_config = config.tasks
        crew_config = config.crew
        inputs = config.input

        input_data = {}
        if isinstance(inputs, list):
            for item in inputs:
                item = item.model_dump()
                input_data[item["key"]] = item["value"]

        agents = []
        for agent_config in agents_config:
            agent_config_without_id = copy.deepcopy(agent_config.dict())
            del agent_config_without_id["id"]
            agent = Agent(**agent_config_without_id)
            agents.append(agent)

        tasks = []
        for task_config in tasks_config:
            task_config_without_agent = copy.deepcopy(task_config.model_dump())
            del task_config_without_agent["agent"]
            del task_config_without_agent["tools"]
            ## Initialize agent with tools
            available_tools = get_available_tools()
            tool_names = available_tools.tool_names
            rprint("🔧 [bold blue]Available tools:[/bold blue]")
            rprint(Pretty(tool_names, expand_all=True))  # Pretty print tool names
            agent = None
            for a in agents_config:
                if a.id == task_config.agent.id:
                    agent_config_without_id = copy.deepcopy(a.model_dump())
                    del agent_config_without_id["id"]
                    agent_config_without_id["tools"] = available_tools.tool_instances
                    agent = Agent(**agent_config_without_id, llm="gpt-4o")
                    break
            task = Task(**task_config_without_agent, agent=agent)
            tasks.append(task)
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=crew_config.verbose,
            memory=crew_config.memory,
        )
        rprint("✅ [bold green]Crew prepared successfully![/bold green]")
        return PreparedCrew(crew=crew, tasks=tasks, input_data=input_data)

    def run_crew_from_config(self, config: CrewConfig) -> CrewOutput:
        """Runs the crew using the specified config and input data."""
        try:
            rprint("🚀 [bold blue]Running crew from config...[/bold blue]")
            prepared_crew = self.__prepare_crew_from_config(config)
            crew = prepared_crew.crew
            crew.kickoff(inputs=prepared_crew.input_data)
            final_result = ""
            for task in prepared_crew.tasks:
                final_result += f"Task: {task.description}\n"
                final_result += f"Output: {task.output.raw}\n"
            rprint("✅ [bold green]Crew run successfully![/bold green]")
            return final_result
        except Exception as e:
            rprint("❌ [bold red]Error running crew![/bold red]")
            traceback.print_exc()
            return f"""
            ## Error: Something went wrong! 😬
            Error Details: 
            
            {str(e)}
            """

    def generate_crew_config(
        self, crew_spec: str
    ) -> Union[CrewConfig, GenerateCrewError]:
        """Generates a crew configuration from the specified crew spec."""
        try:
            rprint("📝 [bold blue]Generating crew configuration...[/bold blue]")
            prompt = f"""
            Generate a crew configuration from the following crew spec:
            Crew Spec: '''{crew_spec}'''
            """
            response = self.ai.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an advanced AI agent for creating and generating agent configurations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format=CrewConfig,
            )
            crew_config = response.choices[0].message.parsed
            rprint(
                "✅ [bold green]Crew configuration generated successfully![/bold green]"
            )
            return crew_config
        except Exception as e:
            rprint("❌ [bold red]Error generating crew configuration![/bold red]")
            return GenerateCrewError(
                error=str(e),
                message="An unexpected error occurred while generating the crew configuration.",
            )

    def pretty_print_config(self, config: CrewConfig) -> None:
        """Pretty prints the crew configuration."""
        rprint("📄 [bold blue]Pretty printing crew configuration...[/bold blue]")
        rprint(Pretty(config.model_dump(), expand_all=True))

    def run(self, prompt: str) -> Any:
        """Runs the Humanoid with the specified prompt."""
        try:
            rprint(
                f"🏃 [bold blue]Running Humanoid with the following prompt: {prompt}[/bold blue]"
            )
            crew_config = self.generate_crew_config(prompt)
            if isinstance(crew_config, GenerateCrewError):
                return {
                    "error": crew_config.error,
                    "message": crew_config.message,
                }
            rprint("🛠️ [bold blue]Crew Config: [/bold blue]")
            self.pretty_print_config(crew_config)  # Call the pretty print method
            rprint("🚀 [bold blue]Running Crew from config...[/bold blue]")
            return self.run_crew_from_config(crew_config)
        except Exception as e:
            rprint("❌ [bold red]Error running Humanoid![/bold red]")
            return {
                "error": str(e),
                "message": "An unexpected error occurred while running the crew.",
            }
