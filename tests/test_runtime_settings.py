from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tempfile
from pathlib import Path

from settings import PhantomSettings, SettingsStore, default_model_for


def main() -> int:
    tmpdir = Path(tempfile.mkdtemp())
    store = SettingsStore(tmpdir / "settings.json")

    original = PhantomSettings(
        provider="google",
        model="",
        google_api_key="abc123",
        openrouter_api_key="or456",
    )
    saved = store.save(original)

    assert saved.provider == "google"
    assert saved.model == default_model_for("google")
    assert saved.google_api_key == "abc123"
    assert saved.openrouter_api_key == "or456"

    loaded = store.load()
    assert loaded.provider == "google"
    assert loaded.model == default_model_for("google")

    print("settings test ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
