"""
tools/filesystem/utils.py
Shared filesystem helpers.
"""

from __future__ import annotations

from datetime import datetime


def human_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size_bytes} B"


def format_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
