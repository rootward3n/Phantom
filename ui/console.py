"""
ui/console.py

Shared Rich console for Phantom.
"""

from __future__ import annotations

import os
import sys

from rich.console import Console

from .theme import PHANTOM_THEME


def _ensure_utf8_terminal() -> None:
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("LANG", "C.UTF-8")
    os.environ.setdefault("LC_ALL", "C.UTF-8")
    os.environ.setdefault("LANGUAGE", "en_US:en")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


_ensure_utf8_terminal()

console = Console(
    soft_wrap=True,
    highlight=False,
    emoji=True,
    theme=PHANTOM_THEME,
)
