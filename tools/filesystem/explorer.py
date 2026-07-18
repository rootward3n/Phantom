"""
tools/filesystem/explorer.py

Directory exploration utilities for Phantom.
"""

from __future__ import annotations

from pathlib import Path

from .utils import human_size, format_timestamp
from .validator import FileSystemValidator


class FileExplorer:
    def __init__(self, validator: FileSystemValidator | None = None):
        self.validator = validator or FileSystemValidator()

    def pwd(self) -> str:
        """Return the current working directory inside the workspace."""
        return self.validator.current_directory()

    def cd(self, target: str) -> str:
        """Change current directory."""
        try:
            path = self.validator.change_directory(target)
            rel = self.validator.relative(path)
            return f"Current directory: {rel}"
        except (FileNotFoundError, NotADirectoryError) as e:
            return str(e)
        except PermissionError as e:
            return str(e)
        except Exception as e:
            return f"CD Error: {e}"

    def home(self) -> str:
        """Return to workspace root."""
        self.validator.reset_directory()
        return "Current directory: /"

    def ls(self, target: str = ".") -> str:
        """List directory contents."""
        try:
            path = self.validator.resolve(target)

            if not path.exists():
                return "Directory not found."

            if not path.is_dir():
                return "Not a directory."

            items = sorted(
                path.iterdir(),
                key=lambda p: (not p.is_dir(), p.name.lower()),
            )

            if not items:
                return "(empty directory)"

            lines = [
                "NAME\tTYPE\tSIZE\tMODIFIED",
                "----\t----\t----\t--------",
            ]

            for item in items:
                stat = item.stat()
                item_type = "DIR" if item.is_dir() else "FILE"
                size = "-" if item.is_dir() else human_size(stat.st_size)
                modified = format_timestamp(stat.st_mtime)

                lines.append(f"{item.name}\t{item_type}\t{size}\t{modified}")

            return "\n".join(lines)

        except PermissionError as e:
            return str(e)
        except Exception as e:
            return f"LS Error: {e}"

    def tree(self, target: str = ".", max_depth: int = 5) -> str:
        """Return a directory tree."""
        try:
            root = self.validator.resolve(target)

            if not root.exists():
                return "Directory not found."

            if not root.is_dir():
                return "Not a directory."

            lines: list[str] = []

            def walk(directory: Path, prefix: str = "", depth: int = 0) -> None:
                if depth >= max_depth:
                    return

                children = sorted(
                    directory.iterdir(),
                    key=lambda p: (not p.is_dir(), p.name.lower()),
                )

                for index, child in enumerate(children):
                    is_last = index == len(children) - 1
                    branch = "└── " if is_last else "├── "
                    icon = "📂 " if child.is_dir() else "📄 "

                    lines.append(prefix + branch + icon + child.name)

                    if child.is_dir():
                        walk(
                            child,
                            prefix + ("    " if is_last else "│   "),
                            depth + 1,
                        )

            root_icon = "📂 " if root.is_dir() else "📄 "
            lines.append(root_icon + root.name)

            walk(root)

            return "\n".join(lines) if lines else "(empty directory)"

        except PermissionError as e:
            return str(e)
        except Exception as e:
            return f"Tree Error: {e}"
