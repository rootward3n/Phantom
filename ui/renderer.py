"""
ui/renderer.py
"""

from __future__ import annotations

from typing import Iterable

from rich import box
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

from .console import console
from .spinner import ThinkingSpinner
from .streaming import iter_smoothed_chunks
from .text_utils import normalize_display_text


def render_streaming_reply(chunks: Iterable[str], *, title: str = "🤖 Phantom") -> str:
    """
    Render a streamed assistant reply using Rich Live Markdown.

    Returns the final accumulated reply text.
    """
    full_reply = ""
    live: Live | None = None
    spinner = ThinkingSpinner()

    spinner.start()

    try:
        for chunk in iter_smoothed_chunks(chunks):
            if not chunk:
                continue

            if live is None:
                spinner.stop()
                live = Live(
                    Panel(
                        Markdown("", code_theme="monokai"),
                        title=f"[bold cyan]{title}[/bold cyan]",
                        border_style="cyan",
                        box=box.ROUNDED,
                        padding=(1, 1),
                    ),
                    console=console,
                    refresh_per_second=20,
                    transient=False,
                )
                live.start()

            full_reply += chunk

            live.update(
                Panel(
                    Markdown(full_reply, code_theme="monokai"),
                    title=f"[bold cyan]{title}[/bold cyan]",
                    border_style="cyan",
                    box=box.ROUNDED,
                    padding=(1, 1),
                )
            )

    finally:
        if live is not None:
            live.stop()
            console.print()
        else:
            spinner.stop()
            console.print("[yellow]⚠ No response returned.[/yellow]")

    return normalize_display_text(full_reply)
