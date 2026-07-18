"""
Safe file copy operations.
"""

import shutil

from .validator import FileSystemValidator


class FileCopier:

    def __init__(self):
        self.validator = FileSystemValidator()

    def copy(self, source: str, destination: str) -> str:

        try:
            src = self.validator.resolve(source)

            if not src.exists():
                return "Source file not found."

            if src.is_dir():
                return "Copying directories is not supported."

            dst = self.validator.ensure_parent(destination)

            shutil.copy2(src, dst)

            return f"Copied '{src.name}' → '{dst.name}'"

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Copy Error: {e}"
