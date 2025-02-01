import unittest
from humanoid.tooling import (
    get_tools_list,
    get_available_tools,
    AvailableTools,
)
from crewai.tools import BaseTool


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
            all(isinstance(tool, BaseTool) for tool in available_tools.tool_instances)
        )


if __name__ == "__main__":
    unittest.main()
