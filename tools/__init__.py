"""
tools/__init__.py

Phantom Tool Framework
"""

from .base import Tool
from .manager import ToolManager, ToolResult

# Core Tools
from .calculator import CalculatorTool
from .time_tool import TimeTool
from .file_tool import FileInfoTool

# File Read / Write
from .read_tool import ReadTool
from .write_tool import WriteTool
from .append_tool import AppendTool

# Directory Tools
from .pwd_tool import PwdTool
from .cd_tool import CdTool
from .home_tool import HomeTool

from .ls_tool import LsTool
from .tree_tool import TreeTool

from .mkdir_tool import MkdirTool
from .rmdir_tool import RmdirTool

# File Management
from .copy_tool import CopyTool
from .move_tool import MoveTool
from .remove_tool import RemoveTool

from .find_tool import FindTool
from .info_tool import InfoTool


__all__ = [
    # Base
    "Tool",
    "ToolManager",
    "ToolResult",

    # Core
    "CalculatorTool",
    "TimeTool",
    "FileInfoTool",

    # Read / Write
    "ReadTool",
    "WriteTool",
    "AppendTool",

    # Workspace
    "PwdTool",
    "CdTool",
    "HomeTool",

    "LsTool",
    "TreeTool",

    "MkdirTool",
    "RmdirTool",

    # File Management
    "CopyTool",
    "MoveTool",
    "RemoveTool",

    "FindTool",
    "InfoTool",
]
