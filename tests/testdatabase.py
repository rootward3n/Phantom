from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database import JsonDatabase

db = JsonDatabase("memory.json")

print("Database Exists :", db.exists())

print("\nInitial Data")
print(db.load())

data = db.load()

data["assistant"] = "Phantom"

db.save(data)

print("\nSaved Data")
print(db.load())
