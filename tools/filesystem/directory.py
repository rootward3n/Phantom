"""
Directory operations for Phantom.
"""

from pathlib import Path

from .validator import FileSystemValidator


class DirectoryManager:

    def __init__(self):
        self.validator = FileSystemValidator()

    def mkdir(self, target: str) -> str:
        try:
            path = self.validator.resolve(target)

            path.mkdir(parents=True, exist_ok=True)

            return f"Directory created: {path.name}"

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Directory Error: {e}"

    def rmdir(self, target: str) -> str:
        try:
            path = self.validator.resolve(target)

            if not path.exists():
                return "Directory not found."

            if not path.is_dir():
                return "Not a directory."

            path.rmdir()

            return f"Directory removed: {path.name}"

        except OSError:
            return "Directory is not empty."

        except Exception as e:
            return f"Directory Error: {e}"
