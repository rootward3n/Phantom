from tools.base import Tool
from tools.filesystem import FileRemover


class RemoveTool(Tool):

    name = "remove"
    description = "Delete a file."

    def __init__(self):
        self.remover = FileRemover()

    def execute(self, arguments: str):

        if not arguments.strip():
            return "Usage: /rm <file>"

        return self.remover.remove(arguments.strip())
