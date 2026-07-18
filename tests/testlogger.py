from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logger import get_logger

logger = get_logger("phantom.test")
logger.info("Logger test started")
logger.warning("This is a warning")
logger.error("This is an error")
print("Logger test complete")
