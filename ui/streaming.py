"""
ui/streaming.py

Helpers for progressively displaying streamed text in a smoother way.
"""

from __future__ import annotations

import re
from typing import Iterable, Iterator

from .text_utils import normalize_display_text


_WORD_SPLIT_RE = re.compile(r"\S+\s*|\s+")


def iter_display_chunks(chunks: Iterable[str]) -> Iterator[str]:
    """
    Expand provider chunks into smaller display chunks.

    Providers may yield large pieces of text. For a smoother streaming effect
    in the CLI/TUI, we split those pieces into smaller word-ish chunks while
    preserving whitespace and line breaks as much as possible.
    """
    for chunk in chunks:
        cleaned = normalize_display_text(chunk)
        if not cleaned:
            continue

        # Short chunks are already visually fine.
        if len(cleaned) <= 24:
            yield cleaned
            continue

        for part in _WORD_SPLIT_RE.findall(cleaned):
            if not part:
                continue

            # If a token is still very long (URLs, file paths, code), break it
            # into smaller visible pieces.
            if len(part) > 48 and not part.isspace():
                step = 16
                for i in range(0, len(part), step):
                    yield part[i : i + step]
            else:
                yield part


def iter_smoothed_chunks(
    chunks: Iterable[str],
    *,
    min_batch_chars: int = 24,
    max_batch_chars: int = 80,
) -> Iterator[str]:
    """
    Batch the display chunks into fewer UI updates.

    This keeps streaming responsive while reducing flicker and repaint churn
    in terminals with slower redraw performance.
    """
    buffer: list[str] = []
    total = 0

    for piece in iter_display_chunks(chunks):
        if not piece:
            continue

        buffer.append(piece)
        total += len(piece)

        should_flush = (
            total >= max_batch_chars
            or (
                total >= min_batch_chars
                and (
                    piece.endswith("\n")
                    or piece.endswith(" ")
                    or piece.endswith("\t")
                    or piece.endswith(".")
                    or piece.endswith("!")
                    or piece.endswith("?")
                    or piece.endswith(",")
                    or piece.endswith(";")
                    or piece.endswith(":")
                )
            )
        )

        if should_flush:
            yield "".join(buffer)
            buffer = []
            total = 0

    if buffer:
        yield "".join(buffer)
