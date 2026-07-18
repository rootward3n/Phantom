"""
runtime.py

Runtime helpers for Phantom's active settings and provider cache.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from settings import PhantomSettings, get_settings, save_settings

if TYPE_CHECKING:
    from providers.google_provider import GoogleProvider
    from providers.openrouter_provider import OpenRouterProvider


@lru_cache(maxsize=8)
def _provider_cache(
    provider: str,
    model: str,
    google_api_key: str,
    openrouter_api_key: str,
    openrouter_app_name: str,
    openrouter_site_url: str,
):
    if provider == "google":
        from providers.google_provider import GoogleProvider

        return GoogleProvider(
            model=model,
            api_key=google_api_key,
        )

    if provider == "openrouter":
        from providers.openrouter_provider import OpenRouterProvider

        return OpenRouterProvider(
            model=model,
            api_key=openrouter_api_key,
            app_name=openrouter_app_name,
            site_url=openrouter_site_url,
        )

    raise ValueError(f"Unsupported provider: {provider}")


def clear_provider_cache() -> None:
    _provider_cache.cache_clear()


def current_settings() -> PhantomSettings:
    return get_settings()


def set_current_settings(settings: PhantomSettings) -> PhantomSettings:
    saved = save_settings(settings)
    clear_provider_cache()
    return saved


def update_current_settings(**changes):
    current = get_settings()
    data = current.to_dict()
    data.update(changes)
    from settings import PhantomSettings

    updated = PhantomSettings.from_dict(data)
    return set_current_settings(updated)


def get_provider(settings: PhantomSettings | None = None):
    current = (settings or get_settings()).normalized()
    return _provider_cache(
        current.provider,
        current.model,
        current.google_api_key,
        current.openrouter_api_key,
        current.openrouter_app_name,
        current.openrouter_site_url,
    )
