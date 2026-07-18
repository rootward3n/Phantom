"""
context.py
Builds the complete prompt sent to the AI.
"""

from prompts import SYSTEM_PROMPT
from memory import Memory
from history import History


memory = Memory()
history = History()


def build_context(user_message: str, include_assistant: bool = True) -> str:
    memories = memory.all()
    history_items = history.last(10)

    prompt = SYSTEM_PROMPT

    if memories:
        prompt += "\n\n=== Memory ===\n"
        for key, value in memories.items():
            prompt += f"{key}: {value}\n"

    if history_items:
        prompt += "\n=== Recent Conversation ===\n"
        for item in history_items:
            prompt += f'{item["role"]}: {item["message"]}\n'

    prompt += "\n=== User ===\n"
    prompt += user_message

    if include_assistant:
        prompt += "\n\nAssistant:"

    return prompt
