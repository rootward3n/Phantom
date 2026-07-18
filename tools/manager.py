"""
tools/manager.py
Tool registry and execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from tools.base import Tool
from tools.calculator import CalculatorTool
from tools.file_tool import FileInfoTool
from tools.time_tool import TimeTool

from tools.read_tool import ReadTool
from tools.write_tool import WriteTool
from tools.append_tool import AppendTool

from tools.mkdir_tool import MkdirTool
from tools.rmdir_tool import RmdirTool

from tools.copy_tool import CopyTool
from tools.move_tool import MoveTool
from tools.remove_tool import RemoveTool

from tools.ls_tool import LsTool
from tools.tree_tool import TreeTool

from tools.pwd_tool import PwdTool
from tools.cd_tool import CdTool
from tools.home_tool import HomeTool

from tools.find_tool import FindTool
from tools.info_tool import InfoTool


@dataclass
class ToolResult:
    handled: bool
    output: str = ""
    error: str = ""


@dataclass
class ToolManager:
    tools: dict[str, Tool] = field(default_factory=dict)

    def __post_init__(self) -> None:

        # Core tools
        self.register(CalculatorTool())
        self.register(TimeTool())
        self.register(FileInfoTool())

        # Filesystem tools
        self.register(ReadTool())
        self.register(WriteTool())
        self.register(AppendTool())

        self.register(MkdirTool())
        self.register(RmdirTool())

        self.register(CopyTool())
        self.register(MoveTool())
        self.register(RemoveTool())

        self.register(LsTool())
        self.register(TreeTool())

        self.register(PwdTool())
        self.register(CdTool())
        self.register(HomeTool())

        self.register(FindTool())
        self.register(InfoTool())

    def register(self, tool: Tool) -> None:
        self.tools[tool.name.lower()] = tool

    def execute(self, command_name: str, arguments: str = "") -> ToolResult:

        tool = self.tools.get(command_name.lower())

        if tool is None:
            return ToolResult(
                handled=False,
                error=f"Unknown tool: {command_name}"
            )

        try:
            output = tool.execute(arguments)

            return ToolResult(
                handled=True,
                output=output
            )

        except Exception as e:
            return ToolResult(
                handled=True,
                error=str(e)
            )

    def list_tools(self) -> list[tuple[str, str]]:
        return [
            (tool.name, tool.description)
            for tool in self.tools.values()
        ]
