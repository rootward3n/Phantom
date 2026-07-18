"""
ui/textual_app.py

Textual TUI for Phantom.
"""

from __future__ import annotations

import asyncio
import threading
from typing import Callable

from rich import box
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.containers import Horizontal
from textual.widgets import Button, Input, RichLog, Static

from runtime import current_settings, set_current_settings
from settings import PhantomSettings, active_model, active_provider_label, available_models, default_model_for, provider_key_status, provider_models

from .banner import phantom_banner
from .panels import shortcuts_panel, status_panel
from .palette import ControlPaletteScreen, SettingsModalScreen
from .streaming import iter_display_chunks
from .text_utils import normalize_display_text


class PhantomTUI(App[None]):
    TITLE = "Phantom"
    SUB_TITLE = "Rich + Textual AI Assistant"
    show_header = False
    show_footer = False

    CSS = """
    Screen {
        background: black;
        color: white;
        layout: vertical;
    }

    Footer {
        display: none;
    }

    Header {
        display: none;
    }

    #banner {
        margin: 1 2 0 2;
    }

    #overview {
        height: auto;
        margin: 1 2 0 2;
    }

    #status_card {
        width: 1fr;
        margin-right: 1;
    }

    #shortcuts_card {
        width: 1fr;
        margin-left: 1;
    }

    #chat_log {
        height: 1fr;
        margin: 1 2 0 2;
        border: round #7f5aa6;
        background: black;
        overflow-y: auto;
    }

    #live_reply {
        display: none;
        height: 10;
        margin: 0 2;
        border: round #1f6feb;
        background: black;
        overflow-y: auto;
    }

    #status_line {
        height: auto;
        margin: 0 2;
        padding: 0 1;
        background: black;
    }

    #prompt_bar {
        height: auto;
        margin: 1 2 1 2;
        background: black;
        min-height: 3;
    }

    #prompt_label {
        width: 12;
        min-width: 12;
        padding: 0 1;
        color: white;
    }

    #prompt_input {
        width: 1fr;
        height: auto;
        background: black;
        border: round #7f5aa6;
        color: white;
    }

    #prompt_input:focus {
        border: round #b68cff;
    }
    """

    BINDINGS = [
        ("ctrl+l", "clear_chat", "Clear chat"),
        ("f1", "open_palette", "Control palette"),
        ("ctrl+s", "open_settings", "Settings"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(
        self,
        *,
        assistant,
        commands,
        stats_provider: Callable[[], dict[str, object]],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.assistant = assistant
        self.commands = commands
        self.stats_provider = stats_provider

        self.banner_view: Static | None = None
        self.status_view: Static | None = None
        self.shortcuts_view: Static | None = None
        self.chat_log: RichLog | None = None
        self.live_reply: Static | None = None
        self.status_line: Static | None = None
        self.prompt: Input | None = None

        self._busy = False
        self._last_submission: tuple[str, float] | None = None

    def compose(self):
        yield Static(phantom_banner(), id="banner")

        with Horizontal(id="overview"):
            yield Static(id="status_card")
            yield Static(id="shortcuts_card")

        yield RichLog(
            id="chat_log",
            wrap=True,
            highlight=False,
            markup=False,
            auto_scroll=True,
        )

        yield Static(id="live_reply")
        yield Static(Text("🟢 Ready", style="bold green"), id="status_line")

        with Horizontal(id="prompt_bar"):
            yield Static("👤 Admin ❯", id="prompt_label")
            yield Input(
                placeholder="type a message or /help",
                id="prompt_input",
            )

    def on_mount(self) -> None:
        self.banner_view = self.query_one("#banner", Static)
        self.status_view = self.query_one("#status_card", Static)
        self.shortcuts_view = self.query_one("#shortcuts_card", Static)
        self.chat_log = self.query_one("#chat_log", RichLog)
        self.live_reply = self.query_one("#live_reply", Static)
        self.status_line = self.query_one("#status_line", Static)
        self.prompt = self.query_one("#prompt_input", Input)

        self._refresh_dashboard()
        self._append_welcome()
        self._clear_live_reply()
        self._set_status("🟢 Ready", "bold green")
        self.prompt.focus()

    def _refresh_dashboard(self) -> None:
        stats = self.stats_provider()
        settings = current_settings().normalized()
        models = provider_models(settings)
        key_status = provider_key_status(settings)

        provider = str(stats.get("provider", active_provider_label(settings)))
        model = str(stats.get("model", active_model(settings)))
        memory_count = int(stats.get("memory_count", 0))
        history_count = int(stats.get("history_count", 0))
        tools_count = int(stats.get("tools_count", 0))
        workspace = str(stats.get("workspace", "."))
        version = str(stats.get("version", "0.1.0"))

        self.status_view.update(
            status_panel(
                provider=provider,
                model=model,
                google_model=models["google"],
                openrouter_model=models["openrouter"],
                memory_count=memory_count,
                history_count=history_count,
                tools_count=tools_count,
                workspace=workspace,
                version=version,
                google_key="set" if key_status["google"] else "missing",
                openrouter_key="set" if key_status["openrouter"] else "missing",
            )
        )
        self.shortcuts_view.update(shortcuts_panel())

    def _append_welcome(self) -> None:
        if self.chat_log is None:
            return

        welcome = Panel(
            Markdown(
                """
# 👻 Welcome to Phantom

Type a message to chat with Phantom.

Use `/palette` or `F1` to change provider, model, and API keys.
                """.strip()
            ),
            title="[bold cyan]🚀 Startup[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 1),
        )
        self.chat_log.write(welcome)

    def _append_user_message(self, message: str) -> None:
        if self.chat_log is None:
            return

        self.chat_log.write(
            Panel(
                Text(normalize_display_text(message)),
                title="[bold green]👤 Admin[/bold green]",
                border_style="green",
                box=box.ROUNDED,
                padding=(1, 1),
            )
        )

    def _append_assistant_message(self, message: str) -> None:
        if self.chat_log is None:
            return

        self.chat_log.write(
            Panel(
                Markdown(normalize_display_text(message) or "_No response returned._"),
                title="[bold cyan]🤖 Phantom[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED,
                padding=(1, 1),
            )
        )

    def _append_system_message(
        self,
        message: str,
        *,
        title: str = "⚙ System",
        border: str = "magenta",
    ) -> None:
        if self.chat_log is None:
            return

        self.chat_log.write(
            Panel(
                Text(normalize_display_text(message)),
                title=f"[bold {border}]{title}[/bold {border}]",
                border_style=border,
                box=box.ROUNDED,
                padding=(1, 1),
            )
        )

    def _set_status(self, message: str, style: str = "bold green") -> None:
        if self.status_line is not None:
            self.status_line.update(Text(message, style=style))

    def _clear_live_reply(self) -> None:
        if self.live_reply is None:
            return

        self.live_reply.styles.display = "none"
        self.live_reply.update(
            Panel(
                Text(" "),
                title="[bold cyan]🤖 Live Reply[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED,
                padding=(1, 1),
            )
        )

    def _update_live_reply(self, message: str) -> None:
        if self.live_reply is None:
            return

        self.live_reply.styles.display = "block"
        self.live_reply.update(
            Panel(
                Text(normalize_display_text(message) or " "),
                title="[bold cyan]🤖 Live Reply[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED,
                padding=(1, 1),
            )
        )

    async def _handle_streaming_chat(self, message: str) -> None:
        if self._busy:
            return

        self._busy = True
        if self.prompt is not None:
            self.prompt.disabled = True

        self._append_user_message(message)
        self._set_status("🤔 Thinking...", "bold yellow")
        self._update_live_reply("🤔 Thinking...")

        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[str | None] = asyncio.Queue()

        def producer() -> None:
            try:
                for chunk in self.assistant.stream_reply(message):
                    if chunk:
                        loop.call_soon_threadsafe(queue.put_nowait, chunk)
            except Exception as exc:
                loop.call_soon_threadsafe(queue.put_nowait, f"\0ERROR\0{exc}")
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)

        threading.Thread(target=producer, daemon=True).start()

        full_reply = ""
        buffer = ""
        last_flush = 0.0

        def flush_buffer(force: bool = False) -> None:
            nonlocal buffer, full_reply, last_flush
            if not buffer:
                return
            if not force and len(buffer) < 48:
                return
            full_reply += buffer
            buffer = ""
            self._update_live_reply(full_reply)
            last_flush = loop.time()

        try:
            while True:
                chunk = await queue.get()
                if chunk is None:
                    break

                if chunk.startswith("\0ERROR\0"):
                    raise RuntimeError(chunk.removeprefix("\0ERROR\0"))

                for part in iter_display_chunks([chunk]):
                    if not part:
                        continue
                    buffer += part
                    now = loop.time()
                    should_flush = (
                        len(buffer) >= 72
                        or (
                            now - last_flush >= 0.12
                            and buffer[-1] in ("\n", " ", "\t", ".", "!", "?", ",", ";", ":")
                        )
                    )
                    if should_flush:
                        flush_buffer()
                    await asyncio.sleep(0)

            flush_buffer(force=True)
            self._append_assistant_message(full_reply)
            self._clear_live_reply()
            self._set_status("🟢 Ready", "bold green")

        except Exception as exc:
            self._clear_live_reply()
            self._append_system_message(
                f"Error: {normalize_display_text(str(exc))}",
                title="❌ Error",
                border="red",
            )
            self._set_status("❌ Error", "bold red")

        finally:
            self._busy = False
            self._last_submission = None
            if self.prompt is not None:
                self.prompt.disabled = False
                self.prompt.value = ""
                self.prompt.focus()
            self._refresh_dashboard()

    async def _save_settings_from_modal(self, payload: dict[str, str]) -> None:
        settings = current_settings().normalized()
        merged = {
            **settings.to_dict(),
            **payload,
        }
        saved = set_current_settings(PhantomSettings.from_dict(merged))
        self._append_system_message(
            f"Settings saved. Provider={active_provider_label(saved)} | Model={saved.model}",
            title="⚙ Settings",
            border="cyan",
        )
        self._refresh_dashboard()

    async def _apply_settings_modal(self, mode: str = "all") -> None:
        await self.push_screen(
            SettingsModalScreen(current_settings().normalized(), mode=mode)
        )

    async def _save_selected_model(self, model: str) -> None:
        settings = current_settings().normalized()
        merged = settings.to_dict()
        if settings.provider == "google":
            merged["google_model"] = model
        else:
            merged["openrouter_model"] = model
        merged["model"] = model
        saved = set_current_settings(PhantomSettings.from_dict(merged))
        self._append_system_message(
            f"Model saved. Provider={active_provider_label(saved)} | Model={saved.model}",
            title="✨ Model",
            border="cyan",
        )
        self._refresh_dashboard()

    async def _open_model_picker(self) -> None:
        settings = current_settings().normalized()
        models = await asyncio.to_thread(
            available_models,
            settings.provider,
            settings,
        )
        await self.push_screen(
            ModelPickerScreen(settings, models)
        )

    async def _open_control_palette(self) -> None:
        await self.push_screen(ControlPaletteScreen(current_settings().normalized()))

    async def _handle_command(self, command: str) -> None:
        self._append_user_message(command)
        self._set_status("⚙ Running command...", "bold magenta")

        result = self.commands.execute(command)

        if result.action == "clear":
            if self.chat_log is not None:
                clear_method = getattr(self.chat_log, "clear", None)
                if callable(clear_method):
                    clear_method()
            self._append_welcome()
            self._clear_live_reply()
            self._set_status("🟢 Ready", "bold green")
            self._refresh_dashboard()
            return

        if result.action == "exit":
            self._append_system_message(
                "👋 Goodbye, Admin.",
                title="👻 Phantom",
                border="yellow",
            )
            self._refresh_dashboard()
            self.exit()
            return

        if result.action == "palette":
            await self._open_control_palette()
            self._set_status("🟢 Ready", "bold green")
            self._refresh_dashboard()
            return

        if result.output:
            self._append_system_message(
                result.output,
                title="⚙ Command Output",
                border="magenta",
            )

        self._set_status("🟢 Ready", "bold green")
        self._refresh_dashboard()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        message = event.value.strip()
        event.input.value = ""

        # Guard against repeated submit events from virtual keyboards,
        # rotation, or accidental double-enter.
        import time as _time
        now = _time.monotonic()
        if self._last_submission is not None:
            last_message, last_time = self._last_submission
            if message == last_message and (now - last_time) < 0.9:
                return
        self._last_submission = (message, now)

        if not message or self._busy:
            return

        if message.startswith("/"):
            await self._handle_command(message)
            return

        await self._handle_streaming_chat(message)

    async def action_open_palette(self) -> None:
        await self._open_control_palette()

    async def action_open_settings(self) -> None:
        await self._apply_settings_modal("all")

    def action_clear_chat(self) -> None:
        if self.chat_log is not None:
            clear_method = getattr(self.chat_log, "clear", None)
            if callable(clear_method):
                clear_method()

        self._append_welcome()
        self._clear_live_reply()
        self._set_status("🟢 Ready", "bold green")
        if self.prompt is not None:
            self.prompt.focus()
        self._refresh_dashboard()
