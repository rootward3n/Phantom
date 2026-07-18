"""
tools/file_tool.py
Basic file information tool.
"""

from __future__ import annotations

from pathlib import Path

from tools.base import Tool


class FileInfoTool(Tool):
    name = "file"
    description = "Show file information."

    def execute(self, arguments: str) -> str:
        target = arguments.strip()

        if not target:
            return "Usage: /file <path>"

        path = Path(target)

        if not path.exists():
            return f"File not found: {target}"

        try:
            stat = path.stat()
            size_kb = stat.st_size / 1024
            modified = path.stat().st_mtime

            return (
                f"Name     : {path.name}\n"
                f"Path     : {path.resolve()}\n"
                f"Size     : {size_kb:.2f} KB\n"
                f"Modified : {modified}"
            )
        except Exception as e:
            return f"File error: {e}"
