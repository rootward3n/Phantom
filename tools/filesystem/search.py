"""
Filesystem search for Phantom.
"""

from fnmatch import fnmatch

from .validator import FileSystemValidator


class FileSearcher:

    def __init__(self):
        self.validator = FileSystemValidator()

    def find(self, pattern: str) -> str:

        workspace = self.validator.workspace
        pattern = pattern.strip()

        if not pattern:
            return "Usage: /find <pattern>"

        matches = []

        wildcard = "*" in pattern or "?" in pattern

        for item in workspace.rglob("*"):

            name = item.name

            if wildcard:
                if fnmatch(name.lower(), pattern.lower()):
                    matches.append(str(item.relative_to(workspace)))
            else:
                if pattern.lower() in name.lower():
                    matches.append(str(item.relative_to(workspace)))

        if not matches:
            return "No matching files found."

        matches.sort()

        return "\n".join(matches)
