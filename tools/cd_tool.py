from tools.base import Tool
from tools.filesystem import FileExplorer


class CdTool(Tool):

    name = "cd"
    description = "Change current directory."

    def __init__(self):
        self.explorer = FileExplorer()

    def execute(self, arguments: str):

        path = arguments.strip()

        if not path:
            return "Usage: /cd <directory>"

        return self.explorer.cd(path)
