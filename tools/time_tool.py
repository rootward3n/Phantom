"""
tools/time_tool.py
Current date/time tool.
"""

from __future__ import annotations

from datetime import datetime

from tools.base import Tool


class TimeTool(Tool):
    name = "time"
    description = "Show current date and time."

    def execute(self, arguments: str) -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
