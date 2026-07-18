from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from memory import Memory

memory = Memory()

memory.remember("name", "Phantom")

memory.remember("creator", "Admin")

print(memory.recall("name"))

print(memory.recall("creator"))

print(memory.all())

print(memory.count())
