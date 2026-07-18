"""
Safe file removal.
"""

from .validator import FileSystemValidator


class FileRemover:

    def __init__(self):
        self.validator = FileSystemValidator()

    def remove(self, target: str) -> str:

        try:
            path = self.validator.resolve(target)

            if not path.exists():
                return "File not found."

            if path.is_dir():
                return "Use /rmdir for directories."

            path.unlink()

            return f"Deleted '{path.name}'"

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Remove Error: {e}"
