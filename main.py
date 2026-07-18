"""
main.py
Phantom CLI
"""

from __future__ import annotations

import argparse
import os
import sys

from assistant import PhantomAssistant
from commands import CommandHandler
from config import APP_VERSION, WORKSPACE_DIR
from history import History
from logger import get_logger
from runtime import current_settings
from settings import active_model, active_provider_label
from tools import ToolManager
from ui import console, render_streaming_reply, startup, user_prompt
from ui.text_utils import normalize_display_text


# Make stdout/stderr friendlier for emoji + UTF-8 terminals.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logger = get_logger("phantom.cli")

history = History()
tools = ToolManager()

commands = CommandHandler(
    memory=None,
    history=history,
    tools=tools,
)

assistant = PhantomAssistant(
    tools=tools,
)


def clear_screen():
    try:
        console.clear()
    except Exception:
        os.system("cls" if os.name == "nt" else "clear")


def startup_stats() -> dict[str, object]:
    settings = current_settings().normalized()
    return {
        "provider": active_provider_label(settings),
        "model": active_model(settings),
        "memory_count": commands.memory.count(),
        "history_count": history.count(),
        "tools_count": len(tools.list_tools()),
        "workspace": str(WORKSPACE_DIR),
        "version": APP_VERSION,
    }


def run_cli() -> int:
    clear_screen()
    startup(**startup_stats())

    logger.info("Phantom started")

    while True:
        try:
            command = user_prompt().strip()

            if not command:
                continue

            # -----------------------------
            # Slash Commands
            # -----------------------------
            if command.startswith("/"):
                logger.info(
                    "Command received: %s",
                    command.split()[0].lower(),
                )

                result = commands.execute(command)

                if result.action == "clear":
                    clear_screen()
                    startup(**startup_stats())
                    logger.info("Screen cleared")
                    continue

                if result.action == "exit":
                    console.print()
                    console.print("[bold cyan]👻 Phantom >[/bold cyan]")
                    console.print("[yellow]👋 Goodbye, Admin.[/yellow]")
                    logger.info("Phantom exited")
                    break

                if result.output:
                    console.print(normalize_display_text(result.output), markup=False)

                continue

            # -----------------------------
            # AI Chat
            # -----------------------------
            history.add("user", command)

            logger.info(
                "User message received chars=%d",
                len(command),
            )

            console.print()
            console.print("[bold cyan]🤖 Phantom >[/bold cyan]")

            full_reply = render_streaming_reply(
                assistant.stream_reply(command),
                title="🤖 Phantom",
            )

            history.add(
                "assistant",
                full_reply,
            )

            logger.info(
                "AI response received chars=%d",
                len(full_reply),
            )

        except KeyboardInterrupt:
            console.print()
            console.print("[yellow]⌨ Interrupted.[/yellow]")
            logger.warning("Phantom interrupted by KeyboardInterrupt")
            break

        except Exception as e:
            console.print()
            console.print(f"[bold red]❌ Error:[/bold red] {normalize_display_text(str(e))}")
            console.print()
            logger.exception("Unhandled exception in main loop")

    return 0


def run_tui() -> int:
    try:
        from ui.textual_app import PhantomTUI
    except Exception as exc:
        console.print(
            "[bold red]❌ Textual TUI could not be started.[/bold red]"
        )
        console.print(
            f"[yellow]Reason:[/yellow] {exc}"
        )
        console.print(
            "[cyan]Install with:[/cyan] pip install textual"
        )
        return 1

    app = PhantomTUI(
        assistant=assistant,
        commands=commands,
        stats_provider=startup_stats,
    )
    app.run()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phantom AI Assistant"
    )
    parser.add_argument(
        "--tui",
        action="store_true",
        help="Launch the Textual TUI instead of the CLI",
    )

    args = parser.parse_args()

    if args.tui:
        return run_tui()

    return run_cli()


if __name__ == "__main__":
    raise SystemExit(main())
