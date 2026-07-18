"""
assistant.py
AI tool-calling orchestration for Phantom.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterator

from brain import ask_raw, stream_ai, stream_raw
from context import build_context
from prompts import build_tool_call_prompt, build_tool_result_prompt
from tools import ToolManager


@dataclass
class ToolPlan:
    tool: str | None = None
    arguments: str = ""
    response: str = ""


class PhantomAssistant:
    def __init__(self, tools: ToolManager | None = None):
        self.tools = tools or ToolManager()

    def _tool_catalog(self) -> list[tuple[str, str]]:
        return self.tools.list_tools()

    def _extract_json(self, text: str) -> dict | None:
        cleaned = text.strip()

        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.S | re.I)
        if fenced:
            cleaned = fenced.group(1).strip()
        else:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                cleaned = cleaned[start : end + 1]

        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return None

        return None

    def _should_attempt_tool_call(self, user_message: str) -> bool:
        message = user_message.lower()

        keywords = [
            "read",
            "write",
            "append",
            "mkdir",
            "rmdir",
            "copy",
            "move",
            "delete",
            "remove",
            "find",
            "info",
            "show file",
            "list files",
            "tree",
            "ls",
            "pwd",
            "cd",
            "home",
            "calculate",
            "calc",
            "time",
            "directory",
            "folder",
            "file",
            "summarize",
        ]

        if any(keyword in message for keyword in keywords):
            return True

        # Path-like or filename-like hints.
        if (
            "/" in message
            or "\\" in message
            or ".py" in message
            or ".md" in message
            or ".txt" in message
        ):
            return True

        return False

    def _plan_tool(self, user_message: str) -> ToolPlan:
        prompt = build_tool_call_prompt(
            user_prompt=user_message,
            tool_catalog=self._tool_catalog(),
            context_text=build_context(user_message, include_assistant=False),
        )

        raw = ask_raw(prompt)
        parsed = self._extract_json(raw)

        if not parsed:
            return ToolPlan(response=raw)

        tool = parsed.get("tool")
        arguments = parsed.get("arguments", "")
        response = parsed.get("response", "")

        if tool is None:
            return ToolPlan(tool=None, response=response or raw)

        if not isinstance(tool, str):
            return ToolPlan(response=raw)

        if isinstance(arguments, dict):
            arguments = json.dumps(arguments, ensure_ascii=False)
        elif arguments is None:
            arguments = ""
        else:
            arguments = str(arguments)

        return ToolPlan(
            tool=tool.strip().lower(),
            arguments=arguments.strip(),
            response=response,
        )

    def stream_reply(self, user_message: str) -> Iterator[str]:
        """Stream the assistant response."""
        if not self._should_attempt_tool_call(user_message):
            yield from stream_ai(user_message)
            return

        plan = self._plan_tool(user_message)

        if not plan.tool:
            yield from stream_ai(user_message)
            return

        tool_result = self.tools.execute(plan.tool, plan.arguments)
        final_tool_output = tool_result.output or tool_result.error or "No result returned."

        followup_prompt = build_tool_result_prompt(
            user_prompt=user_message,
            tool_name=plan.tool,
            arguments=plan.arguments,
            tool_result=final_tool_output,
            context_text=build_context(user_message, include_assistant=False),
        )

        yield from stream_raw(followup_prompt)

    def reply(self, user_message: str) -> str:
        return "".join(self.stream_reply(user_message))
