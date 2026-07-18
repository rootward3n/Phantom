from tools.base import Tool
from tools.filesystem import FileExplorer


class PwdTool(Tool):

    name = "pwd"
    description = "Show current directory."

    def __init__(self):
        self.explorer = FileExplorer()

    def execute(self, arguments: str):
        return self.explorer.pwd()
