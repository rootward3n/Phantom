from tools.base import Tool
from tools.filesystem import FileCopier


class CopyTool(Tool):

    name = "copy"
    description = "Copy a file."

    def __init__(self):
        self.copier = FileCopier()

    def execute(self, arguments: str):

        parts = arguments.split(" ", 1)

        if len(parts) != 2:
            return "Usage: /cp <source> <destination>"

        source, destination = parts

        return self.copier.copy(source, destination)
