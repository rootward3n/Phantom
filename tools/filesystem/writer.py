"""
tools/filesystem/writer.py
Safe file writer for Phantom.
"""

from pathlib import Path

from .validator import FileSystemValidator


class FileWriter:

    def __init__(self):
        self.validator = FileSystemValidator()

    def write(self, target: str, content: str) -> str:
        try:
            path = self.validator.ensure_parent(target)

            path.write_text(
                content,
                encoding="utf-8"
            )

            return f"Written successfully: {path.name}"

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Write Error: {e}"

    def append(self, target: str, content: str) -> str:
        try:
            path = self.validator.ensure_parent(target)

            with open(path, "a", encoding="utf-8") as f:
                f.write(content)

            return f"Appended successfully: {path.name}"

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Append Error: {e}"
