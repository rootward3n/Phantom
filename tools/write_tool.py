from tools.base import Tool
from tools.filesystem import FileWriter


class WriteTool(Tool):

    name = "write"
    description = "Write text to a file."

    def __init__(self):
        self.writer = FileWriter()

    def execute(self, arguments: str) -> str:

        parts = arguments.split(" ", 1)

        if len(parts) < 2:
            return "Usage: /write <file> <text>"

        filename, text = parts

        return self.writer.write(filename, text)
