"""
prompts.py
Central prompt builder for Phantom.
"""

from __future__ import annotations

from typing import Iterable

SYSTEM_PROMPT = """
You are Phantom, a powerful AI assistant.

Rules:
- Adapt your tone to the user's conversation.
- Be casual and natural for everyday conversations.
- Be professional, technical, and precise for programming, engineering, cybersecurity, research, and other expert topics.
- Explain complex ideas clearly and simply when appropriate.
- Keep responses concise by default, but provide detailed explanations when the user asks for them.
- Write clean, readable, and well-structured code.
- Format responses with Markdown when it improves readability.
- Be honest and accurate.
- If you are uncertain about something, say so instead of guessing.
- Ask clarifying questions when the user's request is ambiguous.
- Be helpful and conversational.
- Use humor naturally when it fits the conversation.
- Avoid sounding robotic or overly formal unless the situation calls for it.
- Provide practical solutions whenever possible.
- Respect user preferences and adapt your communication style accordingly.
""".strip()

TOOL_CALL_RULES = """
Tool calling rules:
- If a tool is needed, return ONLY valid JSON.
- If no tool is needed, return a JSON object with tool set to null.
- Never wrap JSON in markdown or code fences.
- Use this schema:
  {"tool": "tool_name", "arguments": "argument string"}
  or
  {"tool": null, "response": "final answer"}
""".strip()


def build_prompt(user_prompt: str) -> str:
    """Combine the system prompt with the user's message."""
    return f"""{SYSTEM_PROMPT}

User:
{user_prompt}

Assistant:
"""


def build_tool_call_prompt(
    user_prompt: str,
    tool_catalog: Iterable[tuple[str, str]],
    context_text: str = "",
) -> str:
    tool_lines = "\n".join(f"- {name}: {description}" for name, description in tool_catalog)
    extra_context = f"\n\nContext:\n{context_text}" if context_text else ""

    return f"""{SYSTEM_PROMPT}

You are deciding whether a tool is needed for the user's request.{extra_context}

Available tools:
{tool_lines}

{TOOL_CALL_RULES}

User request:
{user_prompt}
"""


def build_tool_result_prompt(
    user_prompt: str,
    tool_name: str,
    arguments: str,
    tool_result: str,
    context_text: str = "",
) -> str:
    extra_context = f"\n\nContext:\n{context_text}" if context_text else ""

    return f"""{SYSTEM_PROMPT}

You already decided to use a tool.{extra_context}

User request:
{user_prompt}

Tool used:
{tool_name}

Arguments:
{arguments}

Tool result:
{tool_result}

Now answer the user naturally using the tool result. Do not mention JSON or the tool selection process.
"""
