from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.streaming import iter_smoothed_chunks


def main() -> int:
    chunks = list(iter_smoothed_chunks([
        "Hello ",
        "world! ",
        "This ",
        "is ",
        "Phantom."
    ]))
    assert "".join(chunks) == "Hello world! This is Phantom."
    print("streaming test ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
