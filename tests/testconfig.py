from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import *

print(APP_NAME)
print(APP_VERSION)
print(AUTHOR)
print(ENVIRONMENT)
print(DEBUG)
print(MODEL_NAME)
print(GENERATE_CONTENT_URL)
print(DATA_DIR)
print(LOG_DIR)
