from tools.base import Tool
from tools.filesystem import FileExplorer


class HomeTool(Tool):

    name = "home"
    description = "Return to workspace root."

    def __init__(self):
        self.explorer = FileExplorer()

    def execute(self, arguments: str):
        return self.explorer.home()
