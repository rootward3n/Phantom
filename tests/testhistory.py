from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from history import History

history = History()

history.add("user", "Hello")
history.add("assistant", "Hello Admin!")

print(history.last())
print(history.count())
