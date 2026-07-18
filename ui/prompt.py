"""
ui/prompt.py
"""

from .console import console


def user_prompt() -> str:
    return console.input(
        "[bold green]👤 Admin[/bold green] [cyan]❯[/cyan] "
    )
