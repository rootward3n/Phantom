"""
tools/filesystem/validator.py

Secure filesystem path validator for Phantom.
"""

from __future__ import annotations

from pathlib import Path

from config import WORKSPACE_DIR


class FileSystemValidator:
    """
    Validates all filesystem paths and ensures every operation
    stays inside the Phantom workspace.

    State is shared across all instances so /cd, /pwd and /home
    behave like a real shell across the entire tool framework.
    """

    _shared_workspace: Path | None = None
    _shared_current: Path | None = None

    def __init__(self, workspace: Path | None = None):
        if workspace is None:
            workspace = WORKSPACE_DIR

        workspace = Path(workspace).resolve()

        cls = type(self)

        if cls._shared_workspace is None:
            cls._shared_workspace = workspace
            cls._shared_current = workspace

        self._ensure_state()

    def _ensure_state(self) -> None:
        cls = type(self)

        if cls._shared_workspace is None:
            cls._shared_workspace = Path(WORKSPACE_DIR).resolve()

        if cls._shared_current is None:
            cls._shared_current = cls._shared_workspace

    @property
    def workspace(self) -> Path:
        self._ensure_state()
        return type(self)._shared_workspace  # type: ignore[return-value]

    @workspace.setter
    def workspace(self, value: Path) -> None:
        cls = type(self)
        cls._shared_workspace = Path(value).resolve()

    @property
    def current(self) -> Path:
        self._ensure_state()
        return type(self)._shared_current  # type: ignore[return-value]

    @current.setter
    def current(self, value: Path) -> None:
        cls = type(self)
        cls._shared_current = Path(value).resolve()

    def resolve(self, target: str | Path) -> Path:
        """
        Resolve a user path relative to the current directory.
        """

        path = Path(target).expanduser()

        if not path.is_absolute():
            path = (self.current / path).resolve()
        else:
            path = path.resolve()

        if not self.is_allowed(path):
            raise PermissionError(f"Access denied: {path}")

        return path

    def is_allowed(self, path: Path) -> bool:
        """
        Ensure a path is inside the workspace.
        """

        try:
            path.relative_to(self.workspace)
            return True
        except ValueError:
            return False

    def exists(self, target: str | Path) -> bool:
        """
        Check whether a file or directory exists.
        """

        try:
            return self.resolve(target).exists()
        except Exception:
            return False

    def ensure_parent(self, target: str | Path) -> Path:
        """
        Create parent directories if needed and return the resolved path.
        """

        path = self.resolve(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def change_directory(self, target: str) -> Path:
        """
        Change the current working directory.
        """

        path = self.resolve(target)

        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {target}")

        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {target}")

        self.current = path
        return self.current

    def reset_directory(self) -> Path:
        """
        Return to workspace root.
        """

        self.current = self.workspace
        return self.current

    def relative(self, path: Path) -> str:
        """
        Return workspace-relative path.
        """

        try:
            rel = path.relative_to(self.workspace)
            return "/" if str(rel) == "." else str(rel)
        except ValueError:
            return str(path)

    def current_directory(self) -> str:
        """
        Return current workspace-relative directory.
        """

        rel = self.relative(self.current)
        return rel if rel.startswith("/") else f"/{rel}"
