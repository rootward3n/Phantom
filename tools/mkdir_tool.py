from tools.base import Tool
from tools.filesystem import DirectoryManager


class MkdirTool(Tool):

    name = "mkdir"
    description = "Create a directory."

    def __init__(self):
        self.manager = DirectoryManager()

    def execute(self, arguments: str):

        if not arguments.strip():
            return "Usage: /mkdir <directory>"

        return self.manager.mkdir(arguments.strip())
