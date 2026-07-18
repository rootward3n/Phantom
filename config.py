"""
config.py
Phantom configuration loader.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# -------------------------------------------------------------------
# Terminal / encoding hygiene
# -------------------------------------------------------------------

def _ensure_utf8_environment() -> None:
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("LANG", "C.UTF-8")
    os.environ.setdefault("LC_ALL", "C.UTF-8")
    os.environ.setdefault("LANGUAGE", "en_US:en")


_ensure_utf8_environment()

# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# Workspace Phantom is allowed to access
WORKSPACE_DIR = Path(os.getenv("WORKSPACE_DIR", str(BASE_DIR))).resolve()

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# App settings
# -------------------------------------------------------------------

APP_NAME = os.getenv("APP_NAME", "Phantom").strip() or "Phantom"
APP_VERSION = os.getenv("APP_VERSION", "0.1.0").strip() or "0.1.0"
AUTHOR = os.getenv("AUTHOR", "Admin").strip() or "Admin"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").strip().lower() or "development"
DEBUG = os.getenv("DEBUG", "True").strip().lower() in {"1", "true", "yes", "on"}

# -------------------------------------------------------------------
# AI Provider defaults
# -------------------------------------------------------------------

SUPPORTED_PROVIDERS = {
    "google",
    "openrouter",
}

AI_PROVIDER = os.getenv("AI_PROVIDER", "google").strip().lower() or "google"
if AI_PROVIDER not in SUPPORTED_PROVIDERS:
    AI_PROVIDER = "google"

DEFAULT_GOOGLE_MODEL = "gemma-4-26b-a4b-it"
DEFAULT_OPENROUTER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

MODEL_NAME = os.getenv("MODEL_NAME", "").strip()
if not MODEL_NAME:
    MODEL_NAME = DEFAULT_GOOGLE_MODEL if AI_PROVIDER == "google" else DEFAULT_OPENROUTER_MODEL

# -------------------------------------------------------------------
# API keys / provider metadata
# -------------------------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", APP_NAME).strip() or APP_NAME
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "").strip()

GOOGLE_AI_BASE = "https://generativelanguage.googleapis.com/v1beta"
GENERATE_CONTENT_URL = f"{GOOGLE_AI_BASE}/models/{MODEL_NAME}:generateContent"

OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"
