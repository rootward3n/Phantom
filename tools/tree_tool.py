"""
tools/tree_tool.py
"""

from tools.base import Tool
from tools.filesystem import FileExplorer


class TreeTool(Tool):

    name = "tree"
    description = "Show directory tree."

    def __init__(self):
        self.explorer = FileExplorer()

    def execute(self, arguments: str):
        path = arguments.strip()

        if not path:
            path = "."

        return self.explorer.tree(path)
