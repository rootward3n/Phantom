"""
tools/base.py
Base tool interface for Phantom.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Tool(ABC):
    name: str = "tool"
    description: str = ""

    @abstractmethod
    def execute(self, arguments: str) -> str:
        raise NotImplementedError
