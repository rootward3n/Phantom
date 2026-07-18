"""
Safe file move and rename operations.
"""

import shutil

from .validator import FileSystemValidator


class FileMover:

    def __init__(self):
        self.validator = FileSystemValidator()

    def move(self, source: str, destination: str) -> str:

        try:
            src = self.validator.resolve(source)

            if not src.exists():
                return "Source file not found."

            dst = self.validator.ensure_parent(destination)

            shutil.move(str(src), str(dst))

            return f"Moved '{src.name}' → '{dst.name}'"

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Move Error: {e}"
