"""
ui/text_utils.py

Text normalization helpers for Phantom UI output.
"""

from __future__ import annotations

import unicodedata


_MOJIBAKE_MARKERS = ("Ã", "Â", "â", "ðŸ", "�")

_COMMON_REPLACEMENTS = {
    "â€¢": "•",
    "â€”": "—",
    "â€“": "–",
    "â€˜": "‘",
    "â€™": "’",
    "â€œ": "“",
    "â€": "”",
    "â€¦": "…",
    "Â·": "·",
    "Â°": "°",
    "Â©": "©",
    "Â®": "®",
    "Â£": "£",
    "Â€": "€",
    "Â±": "±",
    "Â¼": "¼",
    "Â½": "½",
    "Â¾": "¾",
    "Â": "",
}


def _apply_common_replacements(text: str) -> str:
    for bad, good in _COMMON_REPLACEMENTS.items():
        text = text.replace(bad, good)
    return text


def normalize_display_text(text: str) -> str:
    """
    Best-effort cleanup for UTF-8/locale mojibake.

    Preserves normal Unicode and emoji, but tries to repair strings that
    were accidentally decoded with the wrong encoding.
    """
    if not text:
        return text

    normalized = unicodedata.normalize("NFC", text)

    if any(marker in normalized for marker in _MOJIBAKE_MARKERS):
        for encoding in ("cp1252", "latin1"):
            try:
                repaired = normalized.encode(encoding).decode("utf-8")
                normalized = repaired
                break
            except Exception:
                continue

    normalized = _apply_common_replacements(normalized)

    # Strip a few common invisible/control artifacts.
    normalized = normalized.replace("\x00", "")
    normalized = normalized.replace("\ufeff", "")

    return normalized
