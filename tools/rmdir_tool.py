from tools.base import Tool
from tools.filesystem import DirectoryManager


class RmdirTool(Tool):

    name = "rmdir"
    description = "Remove an empty directory."

    def __init__(self):
        self.manager = DirectoryManager()

    def execute(self, arguments: str):

        if not arguments.strip():
            return "Usage: /rmdir <directory>"

        return self.manager.rmdir(arguments.strip())
