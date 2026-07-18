"""
Detailed filesystem information for Phantom.
"""

from datetime import datetime
from mimetypes import guess_type

from .utils import human_size, format_timestamp
from .validator import FileSystemValidator


class FileInfo:

    def __init__(self):
        self.validator = FileSystemValidator()

    def get(self, target: str) -> str:

        try:
            path = self.validator.resolve(target)

            if not path.exists():
                return "File not found."

            stat = path.stat()

            mime, _ = guess_type(str(path))
            mime = mime or "Unknown"

            created = datetime.fromtimestamp(
                stat.st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S")

            modified = datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")

            return (
                f"Name       : {path.name}\n"
                f"Type       : {'Directory' if path.is_dir() else 'File'}\n"
                f"Extension  : {path.suffix or '(none)'}\n"
                f"MIME       : {mime}\n"
                f"Size       : {human_size(stat.st_size)}\n"
                f"Created    : {created}\n"
                f"Modified   : {modified}\n"
                f"Path       : {path.relative_to(self.validator.workspace)}\n"
                f"Absolute   : {path.resolve()}"
            )

        except PermissionError as e:
            return str(e)

        except Exception as e:
            return f"Info Error: {e}"
