import unittest
from humanoid.tooling import (
    get_tools_list,
    get_available_tools,
    get_tool,
    AvailableTools,
)
from humanoid.tool_config import ToolType, TOOL_CONFIG


class TestTooling(unittest.TestCase):

    def test_get_tools_list(self):
        tools_list = get_tools_list()
        self.assertIsInstance(tools_list, list)
        self.assertTrue(all(isinstance(tool, str) for tool in tools_list))
        self.assertEqual(len(tools_list), 32)

    def test_get_available_tools(self):
        available_tools = get_available_tools()
        self.assertIsInstance(available_tools, AvailableTools)
        self.assertTrue(
            all(isinstance(tool, str) for tool in available_tools.tool_names)
        )
        self.assertTrue(
            all(
                isinstance(tool, TOOL_CONFIG[ToolType[tool]].get("class"))
                for tool in available_tools.tool_names
            )
        )

    def test_get_tool(self):
        for tool_name in get_tools_list():
            tool_type = ToolType[tool_name]
            tool_config = TOOL_CONFIG.get(tool_type)
            if tool_config:
                args = {
                    arg: "" for arg in tool_config["args"].keys()
                }  # Provide empty strings for simplicity
                tool_instance = get_tool(tool_type, args)
                if tool_instance:
                    self.assertIsInstance(tool_instance, tool_config["class"])

    def test_get_tool_missing_env_var(self):
        for tool_name in get_tools_list():
            tool_type = ToolType[tool_name]
            tool_config = TOOL_CONFIG.get(tool_type)
            if tool_config:
                args = {
                    arg: "" for arg in tool_config["args"].keys()
                }  # Provide empty strings for simplicity
                for env_var in tool_config["env_vars"]:
                    with unittest.mock.patch("os.getenv", return_value=None):
                        tool_instance = get_tool(tool_type, args)
                        self.assertIsNone(tool_instance)

    def test_get_tool_invalid_arg_type(self):
        for tool_name in get_tools_list():
            tool_type = ToolType[tool_name]
            tool_config = TOOL_CONFIG.get(tool_type)
            if tool_config:
                args = {
                    arg: 123 for arg in tool_config["args"].keys()
                }  # Provide invalid type for simplicity
                tool_instance = get_tool(tool_type, args)
                self.assertIsNone(tool_instance)


if __name__ == "__main__":
    unittest.main()
