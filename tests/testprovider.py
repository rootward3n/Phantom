from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from providers.google_provider import GoogleProvider
from providers.openrouter_provider import OpenRouterProvider


def main() -> int:
    google = GoogleProvider(model="demo-google", api_key="demo-key")
    openrouter = OpenRouterProvider(
        model="demo-openrouter",
        api_key="demo-key",
        app_name="Phantom",
        site_url="",
    )

    assert google.config.model == "demo-google"
    assert openrouter.config.model == "demo-openrouter"

    print("provider constructors ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
