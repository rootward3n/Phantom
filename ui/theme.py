"""
ui/theme.py
"""

from rich.theme import Theme

PHANTOM_THEME = Theme(
    {
        "title": "bold cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "assistant": "bold cyan",
        "user": "bold green",
        "info": "cyan",
        "muted": "dim",
        "accent": "bold magenta",
        "ghost": "bright_magenta",
        "panel": "cyan",
    }
)
