"""
database.py
Phantom Database Layer
"""

import json
from pathlib import Path

from config import DATA_DIR


class JsonDatabase:
    """
    Generic JSON database.
    """

    def __init__(self, filename: str):
        self.path = DATA_DIR / filename
        self._initialize()

    def _initialize(self):
        """Create the database file if it doesn't exist."""

        DATA_DIR.mkdir(exist_ok=True)

        if not self.path.exists():
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4)

    def load(self) -> dict:
        """Read JSON data."""

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, data: dict):
        """Write JSON data."""

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def exists(self) -> bool:
        return self.path.exists()

    def clear(self):
        self.save({})
