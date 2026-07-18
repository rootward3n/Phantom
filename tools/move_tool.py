from tools.base import Tool
from tools.filesystem import FileMover


class MoveTool(Tool):

    name = "move"
    description = "Move or rename a file."

    def __init__(self):
        self.mover = FileMover()

    def execute(self, arguments: str):

        parts = arguments.split(" ", 1)

        if len(parts) != 2:
            return "Usage: /mv <source> <destination>"

        source, destination = parts

        return self.mover.move(source, destination)
