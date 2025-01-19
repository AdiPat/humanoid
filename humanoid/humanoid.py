#
# Humanoid: A simple, natural language interface for orchestrating autonomous agents.
# File: humanoid.py
# Author: Aditya Patange (AdiPat)
# License: MIT License
#

import os
import copy
import traceback
from typing import Union, Any

from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from crewai import Agent, Task, Crew
from crewai.crew import CrewOutput


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
        init_result = self.init()
        if init_result.get("error"):
            raise Exception(
                init_result.get("message") + " - Error:" + init_result.get("error")
            )
        self.ai: OpenAI = init_result.get("openai_client", None)

    def init(self) -> dict:
        """Initializes the OpenAI API client."""
        try:
            load_dotenv(dotenv_path=".env", override=True)
            api_key = os.getenv("OPENAI_API_KEY")
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
            return {
                "message": "OpenAI API client initialized successfully.",
                "openai_client": client,
            }
        except Exception as e:
            return {
                "error": str(e),
                "message": "An unexpected error occurred while initializing the OpenAI API client.",
            }

    def run_crew_from_config(self, config: CrewConfig) -> CrewOutput:
        """Runs the crew using the specified config and input data."""
        try:
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
                task_config_without_agent["tools"] = []  # TODO: Implement tools
                agent = None
                for a in agents_config:
                    if a.id == task_config.agent.id:
                        agent_config_without_id = copy.deepcopy(a.dict())
                        del agent_config_without_id["id"]
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

            result = crew.kickoff(inputs=input_data)
            return result
        except Exception as e:
            traceback.print_exc()
            return {
                "error": str(e),
                "message": "An unexpected error occurred while running the crew.",
            }

    def generate_crew_config(
        self, crew_spec: str
    ) -> Union[CrewConfig, GenerateCrewError]:
        """Generates a crew configuration from the specified crew spec."""
        try:
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
            return crew_config
        except Exception as e:
            return GenerateCrewError(
                error=str(e),
                message="An unexpected error occurred while generating the crew configuration.",
            )

    def run(self, prompt: str) -> Any:
        """Runs the Humanoid with the specified prompt."""
        try:
            print(f"Running Humanoid with the following prompt: {prompt}")
            crew_config = self.generate_crew_config(prompt)
            print("Crew Config: ", crew_config.model_dump_json())
            if isinstance(crew_config, GenerateCrewError):
                return {
                    "error": crew_config.error,
                    "message": crew_config.message,
                }
            print("Running Crew from config...")
            return self.run_crew_from_config(crew_config)
        except Exception as e:
            return {
                "error": str(e),
                "message": "An unexpected error occurred while running the crew.",
            }
