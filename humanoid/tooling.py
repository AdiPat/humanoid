#
# Humanoid: A simple, natural language interface for orchestrating autonomous agents.
# File: tooling.py
# Author: Aditya Patange (AdiPat)
# License: MIT License
# ⚡️ "Every instruction, flowing as energy, a fragment of space-time." — AdiPat
#

import os
import logging
import traceback
from pydantic import BaseModel
from crewai.tools import BaseTool
from .tool_config import TOOL_CONFIG, ToolType

logger = logging.getLogger(__name__)


class AvailableTools(BaseModel):
    tool_instances: list[BaseTool]
    tool_names: list[str]


def get_tools_list() -> list[str]:
    """
    Retrieves a list of all tools in the system.
    """
    tools_list = ToolType.__members__.keys()
    return tools_list


def get_available_tools() -> AvailableTools:
    """
    Retrieves the list of available tools and initializes them.
    - Gets a list of all available tools.
    - Initializes each tool.
    - Returns a dictionary of all available tools.
    """
    all_tools = get_tools_list()
    tools = []
    tool_names = []
    for tool in all_tools:
        try:
            tool_instance = get_tool(tool_id=ToolType[tool], args={})
            if tool_instance:
                tools.append(tool_instance)
                tool_names.append(tool)
        except Exception as e:
            logger.error(f"Error while initializing tool {tool}: {str(e)}")
            logger.error(traceback.format_exc())
    return AvailableTools(tool_instances=tools, tool_names=tool_names)


def get_tool(tool_id: ToolType, args: dict) -> BaseTool:
    """
    Initializes a tool based on the specified tool ID using the TOOL_CONFIG.
    """
    tool_config = TOOL_CONFIG.get(tool_id)
    if not tool_config:
        logger.error(f"Tool ID {tool_id} not found.")
        logger.error(f"Supported Tool IDs: {ToolType.__members__}")
        return None

    tool_class = tool_config["class"]
    env_vars = tool_config["env_vars"]
    tool_args = {}

    for env_var in env_vars:
        env_value = os.getenv(env_var)
        if not env_value:
            logger.error(f"{tool_id} tool cannot be initialized: Missing {env_var}.")
            return None
        tool_args[env_var.lower()] = env_value

    for arg, arg_type in tool_config["args"].items():
        arg_value = args.get(arg)
        if arg_value is not None and not isinstance(arg_value, arg_type):
            logger.error(
                f"Invalid type for argument {arg}: expected {arg_type}, got {type(arg_value)}"
            )
            return None
        tool_args[arg] = arg_value

    return tool_class(**tool_args)
