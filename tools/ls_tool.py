"""
tools/ls_tool.py
"""

from tools.base import Tool
from tools.filesystem import FileExplorer


class LsTool(Tool):

    name = "ls"
    description = "List directory contents."

    def __init__(self):
        self.explorer = FileExplorer()

    def execute(self, arguments: str):
        path = arguments.strip()

        if not path:
            path = "."

        return self.explorer.ls(path)
