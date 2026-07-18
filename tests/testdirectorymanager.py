from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.filesystem import DirectoryManager

d = DirectoryManager()

print(d.mkdir("demo"))
print(d.rmdir("demo"))
