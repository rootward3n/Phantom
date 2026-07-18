from tools.base import Tool
from tools.filesystem import FileInfo


class InfoTool(Tool):

    name = "info"
    description = "Show file information."

    def __init__(self):
        self.info = FileInfo()

    def execute(self, arguments: str):

        if not arguments.strip():
            return "Usage: /info <file>"

        return self.info.get(arguments.strip())
