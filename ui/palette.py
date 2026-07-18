"""
ui/palette.py

Textual modals for Phantom's control palette and runtime settings.
"""

from __future__ import annotations

from typing import Literal

from rich import box
from rich.panel import Panel
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static

from settings import (
    PhantomSettings,
    active_model,
    active_provider_label,
    available_models,
    default_model_for,
    provider_key_status,
    provider_models,
)


PaletteAction = Literal[
    "settings",
    "provider",
    "model",
    "keys",
    "refresh",
    "clear",
    "exit",
    "cancel",
]


class ControlPaletteScreen(ModalScreen[None]):
    CSS = """
    ControlPaletteScreen {
        align: center middle;
        background: #000000b3;
    }

    #palette {
        width: 86%;
        max-width: 92;
        max-height: 90%;
        border: round #7f5aa6;
        background: black;
        padding: 1 2;
    }

    #palette_title {
        margin-bottom: 1;
    }

    #action_grid {
        height: auto;
        grid-size: 2;
        grid-gutter: 1 1;
    }

    Button {
        width: 1fr;
    }

    #palette_footer {
        margin-top: 1;
        color: #9aa0a6;
    }
    """

    def __init__(self, settings: PhantomSettings):
        super().__init__()
        self.settings = settings.normalized()

    def compose(self) -> ComposeResult:
        key_status = provider_key_status(self.settings)
        models = provider_models(self.settings)

        stats_table = Table.grid(padding=(0, 1))
        stats_table.add_row(
            "Provider",
            f"{active_provider_label(self.settings)} ({self.settings.provider})",
        )
        stats_table.add_row("Active model", active_model(self.settings))
        stats_table.add_row("Google key", "set" if key_status["google"] else "missing")
        stats_table.add_row(
            "OpenRouter key",
            "set" if key_status["openrouter"] else "missing",
        )
        stats_table.add_row("Google model", models["google"])
        stats_table.add_row("OpenRouter model", models["openrouter"])

        with Container(id="palette"):
            yield Static(
                Panel(
                    stats_table,
                    title="[bold cyan]🎛 Control Palette[/bold cyan]",
                    border_style="cyan",
                    box=box.ROUNDED,
                    padding=(0, 1),
                ),
                id="palette_title",
            )
            with Horizontal(id="action_grid"):
                yield Button("Settings", id="settings", variant="primary")
                yield Button("Provider", id="provider")
                yield Button("Model", id="model")
                yield Button("API Keys", id="keys")
                yield Button("Refresh", id="refresh")
                yield Button("Clear Chat", id="clear")
                yield Button("Exit", id="exit", variant="error")
            yield Static(
                "Use the buttons above, or press Esc to close.",
                id="palette_footer",
            )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        action = event.button.id
        self.dismiss(None)

        if action == "settings":
            await self.app._apply_settings_modal("all")
        elif action == "provider":
            await self.app._apply_settings_modal("provider")
        elif action == "model":
            await self.app._open_model_picker()
        elif action == "keys":
            await self.app._apply_settings_modal("keys")
        elif action == "refresh":
            self.app._refresh_dashboard()
        elif action == "clear":
            self.app.action_clear_chat()
        elif action == "exit":
            self.app.exit()

    def on_key(self, event) -> None:
        if getattr(event, "key", None) == "escape":
            self.dismiss(None)


class SettingsModalScreen(ModalScreen[None]):
    CSS = """
    SettingsModalScreen {
        align: center middle;
        background: #000000b3;
    }

    #settings_modal {
        width: 92%;
        max-width: 104;
        max-height: 92%;
        border: round #1f6feb;
        background: black;
        padding: 1 2;
    }

    #settings_body {
        height: auto;
    }

    .field {
        height: auto;
        margin-bottom: 1;
    }

    .field_label {
        color: #c9d1d9;
        margin-bottom: 0;
    }

    Input, Select {
        width: 1fr;
    }

    #settings_buttons {
        height: auto;
        margin-top: 1;
        layout: horizontal;
    }

    #settings_buttons Button {
        width: 1fr;
        margin-right: 1;
    }
    """

    def __init__(self, settings: PhantomSettings, mode: str = "all"):
        super().__init__()
        self.settings = settings.normalized()
        self.mode = mode

    def compose(self) -> ComposeResult:
        models = provider_models(self.settings)

        with Container(id="settings_modal"):
            yield Static(
                Panel(
                    f"[bold cyan]Provider[/bold cyan]: {active_provider_label(self.settings)} ({self.settings.provider})\n"
                    f"[bold cyan]Active model[/bold cyan]: {active_model(self.settings)}\n"
                    f"[bold cyan]Mode[/bold cyan]: {self.mode}\n"
                    "\nEdit the fields and press Save.",
                    title="[bold cyan]⚙ Runtime Settings[/bold cyan]",
                    border_style="cyan",
                    box=box.ROUNDED,
                    padding=(0, 1),
                )
            )
            with VerticalScroll(id="settings_body"):
                with Container(classes="field"):
                    yield Static("Provider", classes="field_label")
                    yield Select.from_values(
                        ["google", "openrouter"],
                        prompt="Provider",
                        value=self.settings.provider,
                        allow_blank=False,
                        id="provider_select",
                    )

                with Container(classes="field"):
                    yield Static("Google model", classes="field_label")
                    yield Input(
                        value=self.settings.google_model or default_model_for("google"),
                        placeholder=default_model_for("google"),
                        id="google_model",
                    )

                with Container(classes="field"):
                    yield Static("OpenRouter model", classes="field_label")
                    yield Input(
                        value=self.settings.openrouter_model
                        or default_model_for("openrouter"),
                        placeholder=default_model_for("openrouter"),
                        id="openrouter_model",
                    )

                with Container(classes="field"):
                    yield Static("Google API key", classes="field_label")
                    yield Input(
                        value=self.settings.google_api_key,
                        placeholder="Paste GOOGLE_API_KEY",
                        password=True,
                        id="google_key",
                    )

                with Container(classes="field"):
                    yield Static("OpenRouter API key", classes="field_label")
                    yield Input(
                        value=self.settings.openrouter_api_key,
                        placeholder="Paste OPENROUTER_API_KEY",
                        password=True,
                        id="openrouter_key",
                    )

                with Container(classes="field"):
                    yield Static("OpenRouter app name", classes="field_label")
                    yield Input(
                        value=self.settings.openrouter_app_name,
                        placeholder="Phantom",
                        id="openrouter_app_name",
                    )

                with Container(classes="field"):
                    yield Static("OpenRouter site URL", classes="field_label")
                    yield Input(
                        value=self.settings.openrouter_site_url,
                        placeholder="https://example.com",
                        id="openrouter_site_url",
                    )

                yield Static(
                    f"Detected models: Google={models['google']} | OpenRouter={models['openrouter']}",
                    id="settings_hint",
                )

            with Horizontal(id="settings_buttons"):
                yield Button("Save", id="save", variant="primary")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        focus_map = {
            "provider": "provider_select",
            "model": "google_model" if self.settings.provider == "google" else "openrouter_model",
            "keys": "google_key" if self.settings.provider == "google" else "openrouter_key",
        }
        target = focus_map.get(self.mode, "provider_select")
        widget = self.query_one(f"#{target}")
        widget.focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
            return

        if event.button.id != "save":
            return

        provider = self.query_one("#provider_select", Select).value or self.settings.provider
        google_model = self.query_one("#google_model", Input).value.strip()
        openrouter_model = self.query_one("#openrouter_model", Input).value.strip()
        google_key = self.query_one("#google_key", Input).value.strip()
        openrouter_key = self.query_one("#openrouter_key", Input).value.strip()
        openrouter_app_name = self.query_one("#openrouter_app_name", Input).value.strip()
        openrouter_site_url = self.query_one("#openrouter_site_url", Input).value.strip()

        payload = {
            "provider": str(provider),
            "google_model": google_model,
            "openrouter_model": openrouter_model,
            "google_api_key": google_key,
            "openrouter_api_key": openrouter_key,
            "openrouter_app_name": openrouter_app_name,
            "openrouter_site_url": openrouter_site_url,
        }

        self.dismiss(None)
        await self.app._save_settings_from_modal(payload)

    def on_key(self, event) -> None:
        if getattr(event, "key", None) == "escape":
            self.dismiss(None)


class ModelPickerScreen(ModalScreen[None]):
    CSS = """
    ModelPickerScreen {
        align: center middle;
        background: #000000b3;
    }

    #model_modal {
        width: 92%;
        max-width: 104;
        max-height: 92%;
        border: round #7f5aa6;
        background: black;
        padding: 1 2;
    }

    #model_list {
        height: auto;
        margin-top: 1;
    }

    Input, Select {
        width: 1fr;
    }

    #model_buttons {
        height: auto;
        margin-top: 1;
        layout: horizontal;
    }

    #model_buttons Button {
        width: 1fr;
        margin-right: 1;
    }
    """

    def __init__(self, settings: PhantomSettings, models: list[str]):
        super().__init__()
        self.settings = settings.normalized()
        self.models = models or [self.settings.model or default_model_for(self.settings.provider)]

    def compose(self) -> ComposeResult:
        provider_name = active_provider_label(self.settings)
        current_model_name = self.settings.model or default_model_for(self.settings.provider)
        selected = current_model_name if current_model_name in self.models else self.models[0]

        with Container(id="model_modal"):
            yield Static(
                Panel(
                    f"[bold cyan]Provider[/bold cyan]: {provider_name} ({self.settings.provider})\n"
                    f"[bold cyan]Current model[/bold cyan]: {current_model_name}\n"
                    f"[bold cyan]Available models[/bold cyan]: {len(self.models)}",
                    title="[bold cyan]✨ Model Picker[/bold cyan]",
                    border_style="cyan",
                    box=box.ROUNDED,
                    padding=(0, 1),
                )
            )
            with VerticalScroll(id="model_list"):
                yield Static("Choose a model from the provider list:", classes="field_label")
                yield Select.from_values(
                    self.models,
                    value=selected,
                    allow_blank=False,
                    id="model_select",
                )

            with Horizontal(id="model_buttons"):
                yield Button("Save", id="save", variant="primary")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#model_select", Select).focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
            return

        if event.button.id != "save":
            return

        selected = str(self.query_one("#model_select", Select).value or "").strip()
        if not selected:
            self.dismiss(None)
            return

        self.dismiss(None)
        await self.app._save_selected_model(selected)

    def on_key(self, event) -> None:
        if getattr(event, "key", None) == "escape":
            self.dismiss(None)
