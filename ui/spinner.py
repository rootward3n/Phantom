"""
ui/spinner.py
"""

from __future__ import annotations

from contextlib import AbstractContextManager

from rich.status import Status

from .console import console


class ThinkingSpinner(AbstractContextManager):
    def __init__(self, message: str = "[bold cyan]🤔 Thinking...[/bold cyan]"):
        self._status: Status = console.status(message, spinner="dots")

    def start(self) -> None:
        self._status.start()

    def stop(self) -> None:
        self._status.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()
        return False
