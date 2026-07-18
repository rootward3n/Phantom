from tools.base import Tool
from tools.filesystem import FileReader


class ReadTool(Tool):

    name = "read"
    description = "Read a text file."

    def __init__(self):
        self.reader = FileReader()

    def execute(self, arguments: str) -> str:

        if not arguments.strip():
            return "Usage: /read <file>"

        return self.reader.read(arguments.strip())
