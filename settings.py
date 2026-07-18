"""
settings.py

Persistent runtime settings for Phantom.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from config import (
    AI_PROVIDER as ENV_AI_PROVIDER,
    APP_NAME,
    DATA_DIR,
    DEFAULT_GOOGLE_MODEL,
    DEFAULT_OPENROUTER_MODEL,
    GOOGLE_API_KEY as ENV_GOOGLE_API_KEY,
    MODEL_NAME as ENV_MODEL_NAME,
    OPENROUTER_API_KEY as ENV_OPENROUTER_API_KEY,
    OPENROUTER_APP_NAME as ENV_OPENROUTER_APP_NAME,
    OPENROUTER_SITE_URL as ENV_OPENROUTER_SITE_URL,
    SUPPORTED_PROVIDERS,
)

SETTINGS_FILE = DATA_DIR / "settings.json"

PROVIDER_LABELS: dict[str, str] = {
    "google": "Google AI Studio",
    "openrouter": "OpenRouter",
}


def _normalize_provider(value: str | None) -> str:
    provider = (value or "").strip().lower()
    if provider not in SUPPORTED_PROVIDERS:
        return ENV_AI_PROVIDER if ENV_AI_PROVIDER in SUPPORTED_PROVIDERS else "google"
    return provider


def provider_label(provider: str | None = None) -> str:
    normalized = _normalize_provider(provider or ENV_AI_PROVIDER)
    return PROVIDER_LABELS.get(normalized, normalized.replace("_", " ").title())


def default_model_for(provider: str) -> str:
    provider = _normalize_provider(provider)
    if provider == "openrouter":
        return DEFAULT_OPENROUTER_MODEL
    return DEFAULT_GOOGLE_MODEL


def provider_model(settings: "PhantomSettings" | None, provider: str) -> str:
    current = settings.normalized() if settings else get_settings().normalized()
    normalized = _normalize_provider(provider)
    if normalized == "openrouter":
        return current.openrouter_model or default_model_for("openrouter")
    return current.google_model or default_model_for("google")


def active_provider_label(settings: "PhantomSettings" | None = None) -> str:
    current = settings.normalized() if settings else get_settings().normalized()
    return provider_label(current.provider)


def active_model(settings: "PhantomSettings" | None = None) -> str:
    current = settings.normalized() if settings else get_settings().normalized()
    return current.model


@dataclass(slots=True)
class PhantomSettings:
    provider: str = "google"
    model: str = ""
    google_model: str = ""
    openrouter_model: str = ""
    google_api_key: str = ""
    openrouter_api_key: str = ""
    openrouter_app_name: str = APP_NAME
    openrouter_site_url: str = ""

    def normalized(self) -> "PhantomSettings":
        provider = _normalize_provider(self.provider)

        google_model = self.google_model.strip()
        openrouter_model = self.openrouter_model.strip()
        fallback_model = self.model.strip()

        if provider == "google":
            active_model_value = google_model or fallback_model or default_model_for("google")
            google_model = active_model_value
            if not openrouter_model:
                openrouter_model = default_model_for("openrouter")
        else:
            active_model_value = openrouter_model or fallback_model or default_model_for("openrouter")
            openrouter_model = active_model_value
            if not google_model:
                google_model = default_model_for("google")

        return PhantomSettings(
            provider=provider,
            model=active_model_value,
            google_model=google_model,
            openrouter_model=openrouter_model,
            google_api_key=self.google_api_key.strip(),
            openrouter_api_key=self.openrouter_api_key.strip(),
            openrouter_app_name=self.openrouter_app_name.strip() or APP_NAME,
            openrouter_site_url=self.openrouter_site_url.strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self.normalized())

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "PhantomSettings":
        data = data or {}

        provider = _normalize_provider(str(data.get("provider", ENV_AI_PROVIDER)))
        active_model_value = str(data.get("model", ENV_MODEL_NAME)).strip()

        google_model = str(data.get("google_model", "")).strip()
        openrouter_model = str(data.get("openrouter_model", "")).strip()

        if not google_model:
            google_model = (
                active_model_value
                if provider == "google" and active_model_value
                else default_model_for("google")
            )

        if not openrouter_model:
            openrouter_model = (
                active_model_value
                if provider == "openrouter" and active_model_value
                else default_model_for("openrouter")
            )

        return cls(
            provider=provider,
            model=active_model_value or default_model_for(provider),
            google_model=google_model,
            openrouter_model=openrouter_model,
            google_api_key=str(data.get("google_api_key", ENV_GOOGLE_API_KEY)).strip(),
            openrouter_api_key=str(
                data.get("openrouter_api_key", ENV_OPENROUTER_API_KEY)
            ).strip(),
            openrouter_app_name=str(
                data.get("openrouter_app_name", ENV_OPENROUTER_APP_NAME)
            ).strip() or APP_NAME,
            openrouter_site_url=str(
                data.get("openrouter_site_url", ENV_OPENROUTER_SITE_URL)
            ).strip(),
        ).normalized()

    def has_api_key(self, provider: str | None = None) -> bool:
        provider_name = _normalize_provider(provider or self.provider)
        if provider_name == "google":
            return bool(self.google_api_key)
        if provider_name == "openrouter":
            return bool(self.openrouter_api_key)
        return False

    def redacted(self) -> dict[str, Any]:
        data = self.to_dict()
        if data.get("google_api_key"):
            data["google_api_key"] = _redact_secret(data["google_api_key"])
        if data.get("openrouter_api_key"):
            data["openrouter_api_key"] = _redact_secret(data["openrouter_api_key"])
        return data


def _redact_secret(secret: str) -> str:
    if len(secret) <= 8:
        return "*" * len(secret)
    return f"{secret[:4]}…{secret[-4:]}"


class SettingsStore:
    def __init__(self, path: Path | None = None):
        self.path = path or SETTINGS_FILE

    def load(self) -> PhantomSettings:
        base = PhantomSettings.from_dict(
            {
                "provider": ENV_AI_PROVIDER,
                "model": ENV_MODEL_NAME,
                "google_model": ENV_MODEL_NAME if _normalize_provider(ENV_AI_PROVIDER) == "google" else DEFAULT_GOOGLE_MODEL,
                "openrouter_model": ENV_MODEL_NAME if _normalize_provider(ENV_AI_PROVIDER) == "openrouter" else DEFAULT_OPENROUTER_MODEL,
                "google_api_key": ENV_GOOGLE_API_KEY,
                "openrouter_api_key": ENV_OPENROUTER_API_KEY,
                "openrouter_app_name": ENV_OPENROUTER_APP_NAME,
                "openrouter_site_url": ENV_OPENROUTER_SITE_URL,
            }
        )

        if not self.path.exists():
            return base.normalized()

        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                stored = json.load(handle)
        except Exception:
            return base.normalized()

        merged = base.to_dict()
        if isinstance(stored, dict):
            for key, value in stored.items():
                if key in merged:
                    merged[key] = value

        return PhantomSettings.from_dict(merged).normalized()

    def save(self, settings: PhantomSettings) -> PhantomSettings:
        normalized = settings.normalized()
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(
                normalized.to_dict(),
                handle,
                indent=2,
                ensure_ascii=False,
            )

        return normalized

    def update(self, **changes: Any) -> PhantomSettings:
        current = self.load()
        data = current.to_dict()
        data.update(changes)
        updated = PhantomSettings.from_dict(data).normalized()
        return self.save(updated)


_store = SettingsStore()


def get_settings() -> PhantomSettings:
    return _store.load()


def save_settings(settings: PhantomSettings) -> PhantomSettings:
    return _store.save(settings)


def update_settings(**changes: Any) -> PhantomSettings:
    return _store.update(**changes)


def settings_path() -> Path:
    return _store.path


def provider_key_status(settings: PhantomSettings | None = None) -> dict[str, bool]:
    current = settings.normalized() if settings else get_settings()
    return {
        "google": bool(current.google_api_key),
        "openrouter": bool(current.openrouter_api_key),
    }


def provider_models(settings: PhantomSettings | None = None) -> dict[str, str]:
    current = settings.normalized() if settings else get_settings()
    return {
        "google": current.google_model or default_model_for("google"),
        "openrouter": current.openrouter_model or default_model_for("openrouter"),
    }


def available_models(
    provider: str | None = None,
    settings: PhantomSettings | None = None,
) -> list[str]:
    """Return model choices for a provider, falling back safely when discovery fails."""
    current = settings.normalized() if settings else get_settings().normalized()
    provider_name = _normalize_provider(provider or current.provider)
    fallback = provider_model(current, provider_name)
    defaults = [fallback, default_model_for(provider_name)]

    unique_defaults: list[str] = []
    for item in defaults:
        cleaned = item.strip()
        if cleaned and cleaned not in unique_defaults:
            unique_defaults.append(cleaned)

    try:
        if provider_name == "google":
            from providers.google_provider import GoogleProvider

            models = GoogleProvider(
                model=fallback,
                api_key=current.google_api_key,
            ).list_models()
        elif provider_name == "openrouter":
            from providers.openrouter_provider import OpenRouterProvider

            models = OpenRouterProvider(
                model=fallback,
                api_key=current.openrouter_api_key,
                app_name=current.openrouter_app_name,
                site_url=current.openrouter_site_url,
            ).list_models()
        else:
            models = []
    except Exception:
        models = []

    normalized: list[str] = []
    for model in models:
        cleaned = str(model).strip()
        if cleaned and cleaned not in normalized:
            normalized.append(cleaned)

    for item in reversed(unique_defaults):
        if item not in normalized:
            normalized.insert(0, item)

    return normalized or unique_defaults
