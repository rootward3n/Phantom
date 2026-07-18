"""
brain.py
High-level AI interface for Phantom.
"""

from __future__ import annotations

from runtime import get_provider


def ask_ai(prompt: str) -> str:
    """
    Return a complete AI response.
    """
    return get_provider().ask(prompt)


def stream_ai(prompt: str):
    """
    Yield streamed AI response chunks.
    """
    yield from get_provider().stream(prompt)


def ask_raw(prompt: str) -> str:
    """
    Return a complete response without prompt wrapping.
    """
    return get_provider().ask_raw(prompt)


def stream_raw(prompt: str):
    """
    Yield streamed response chunks without prompt wrapping.
    """
    yield from get_provider().stream_raw(prompt)
