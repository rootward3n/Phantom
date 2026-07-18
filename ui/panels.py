"""
ui/panels.py
"""

from __future__ import annotations

from rich import box
from rich.panel import Panel
from rich.table import Table


def status_panel(
    *,
    provider: str = "Google AI Studio",
    model: str = "Gemini 2.5 Flash",
    google_model: str = "",
    openrouter_model: str = "",
    memory_count: int = 0,
    history_count: int = 0,
    tools_count: int = 0,
    workspace: str = ".",
    version: str = "0.1.0",
    google_key: str = "missing",
    openrouter_key: str = "missing",
):
    table = Table.grid(padding=(0, 2))
    table.add_row("🟢 Status", "[green]ONLINE[/green]")
    table.add_row("🤖 AI Core", "[green]CONNECTED[/green]")
    table.add_row("☁ Provider", f"[cyan]{provider}[/cyan]")
    table.add_row("✨ Active model", f"[magenta]{model}[/magenta]")

    if google_model:
        table.add_row("🔵 Google model", f"[dim]{google_model}[/dim]")
    if openrouter_model:
        table.add_row("🟣 OpenRouter model", f"[dim]{openrouter_model}[/dim]")

    table.add_row("🔐 Google key", f"[cyan]{google_key}[/cyan]")
    table.add_row("🔐 OpenRouter key", f"[cyan]{openrouter_key}[/cyan]")
    table.add_row("💾 Memory", f"[cyan]{memory_count} item(s)[/cyan]")
    table.add_row("🧠 History", f"[cyan]{history_count} item(s)[/cyan]")
    table.add_row("🛠 Tools", f"[cyan]{tools_count} available[/cyan]")
    table.add_row("📁 Workspace", f"[dim]{workspace}[/dim]")
    table.add_row("🏷 Version", f"[dim]{version}[/dim]")

    return Panel(
        table,
        title="[bold cyan]System[/bold cyan]",
        border_style="green",
        box=box.ROUNDED,
        padding=(0, 1),
    )


def shortcuts_panel():
    table = Table.grid(padding=(0, 2))
    table.add_row("⌨ /help", "Show commands")
    table.add_row("🎛 /palette", "Open control palette")
    table.add_row("☁ /providers", "List providers")
    table.add_row("🔁 /provider", "Set active provider")
    table.add_row("✨ /model", "Set active model")
    table.add_row("🔐 /keys", "Show or set API keys")
    table.add_row("⚙ /settings", "Show runtime settings")
    table.add_row("📚 /read", "Read a workspace file")
    table.add_row("✍ /write", "Write text to a file")
    table.add_row("➕ /append", "Append text to a file")
    table.add_row("📂 /ls", "List directory contents")
    table.add_row("🌲 /tree", "Show directory tree")
    table.add_row("🧭 /pwd", "Show current directory")
    table.add_row("📁 /cd", "Change current directory")
    table.add_row("🏠 /home", "Return to workspace root")
    table.add_row("⌨ F1", "Open control palette")
    table.add_row("⌨ Ctrl+L", "Clear chat")
    table.add_row("⌨ Ctrl+Q", "Quit")

    return Panel(
        table,
        title="[bold cyan]Quick Commands[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 1),
    )
