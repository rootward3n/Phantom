"""
ui/startup.py
"""

from __future__ import annotations

from rich.console import Group
from rich.padding import Padding

from config import APP_VERSION
from runtime import current_settings
from settings import active_model, active_provider_label, provider_key_status, provider_models

from .banner import phantom_banner
from .console import console
from .panels import shortcuts_panel, status_panel


def startup(
    *,
    provider: str = "Google AI Studio",
    model: str = "",
    memory_count: int = 0,
    history_count: int = 0,
    tools_count: int = 0,
    workspace: str = ".",
    version: str = APP_VERSION,
):
    settings = current_settings().normalized()
    key_status = provider_key_status(settings)
    models = provider_models(settings)

    console.print()

    console.print(
        Group(
            phantom_banner(),
            Padding(
                status_panel(
                    provider=provider or active_provider_label(settings),
                    model=model or active_model(settings),
                    google_model=models["google"],
                    openrouter_model=models["openrouter"],
                    memory_count=memory_count,
                    history_count=history_count,
                    tools_count=tools_count,
                    workspace=workspace,
                    version=version,
                    google_key="set" if key_status["google"] else "missing",
                    openrouter_key="set" if key_status["openrouter"] else "missing",
                ),
                (1, 0, 0, 0),
            ),
            Padding(shortcuts_panel(), (1, 0, 0, 0)),
        )
    )

    console.print()
