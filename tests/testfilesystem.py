from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.filesystem import FileSystemValidator, FileExplorer

validator = FileSystemValidator()
explorer = FileExplorer(validator)

print("Workspace:", explorer.pwd())
print("\nLS:\n", explorer.ls("."))
print("\nTREE:\n", explorer.tree("."))
