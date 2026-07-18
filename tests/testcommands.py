from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from commands import CommandHandler
from history import History

handler = CommandHandler(history=History())

print(handler.execute("/help").output)
print(handler.execute("/status").output)
print(handler.execute('/remember favorite_language Python').output)
print(handler.execute("/memory").output)
print(handler.execute("/forget favorite_language").output)
print(handler.execute("/memory").output)
