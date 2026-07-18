from tools.base import Tool
from tools.filesystem import FileSearcher


class FindTool(Tool):

    name = "find"
    description = "Search files."

    def __init__(self):
        self.searcher = FileSearcher()

    def execute(self, arguments: str):

        if not arguments.strip():
            return "Usage: /find <pattern>"

        return self.searcher.find(arguments.strip())
