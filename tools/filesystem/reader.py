"""
tools/filesystem/reader.py
Safe file reader for Phantom.
"""

from pathlib import Path

from .validator import FileSystemValidator


class FileReader:

    def __init__(self):
        self.validator = FileSystemValidator()

    def read(self, target: str) -> str:

        try:
            path = self.validator.resolve(target)

            if not path.exists():
                return f"File not found: {target}"

            if path.is_dir():
                return "Cannot read a directory."

            return path.read_text(
                encoding="utf-8",
                errors="replace"
            )

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Read Error: {e}"
