"""
providers/openrouter_provider.py

OpenRouter provider for Phantom.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterator

import requests

from config import OPENROUTER_BASE
from context import build_context
from logger import get_logger

logger = get_logger("phantom.openrouter")


@dataclass(slots=True)
class OpenRouterProviderConfig:
    model: str
    api_key: str
    app_name: str
    site_url: str


class OpenRouterProvider:
    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        app_name: str,
        site_url: str,
    ):
        self.config = OpenRouterProviderConfig(
            model=model,
            api_key=api_key,
            app_name=app_name,
            site_url=site_url,
        )

    def _headers(self) -> dict[str, str]:
        if not self.config.api_key:
            raise ValueError(
                "OpenRouter API key is missing. Open /settings and add OPENROUTER_API_KEY."
            )

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "X-Title": self.config.app_name,
        }

        if self.config.site_url:
            headers["HTTP-Referer"] = self.config.site_url

        return headers

    def _payload(self, prompt: str, *, stream: bool) -> dict:
        return {
            "model": self.config.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": stream,
        }

    def _post(self, prompt: str, *, stream: bool):
        response = requests.post(
            OPENROUTER_BASE,
            headers=self._headers(),
            json=self._payload(prompt, stream=stream),
            stream=stream,
            timeout=120,
        )
        response.encoding = "utf-8"
        response.raise_for_status()
        return response


    def list_models(self) -> list[str]:
        """Return available OpenRouter model IDs."""
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers=self._headers() if self.config.api_key else {},
                timeout=60,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network/runtime guard
            logger.warning("Could not list OpenRouter models: %s", exc)
            return [self.config.model]

        models: list[str] = []
        for item in payload.get("data", []) if isinstance(payload, dict) else []:
            if not isinstance(item, dict):
                continue
            name = str(item.get("id") or item.get("slug") or item.get("name") or "").strip()
            if not name:
                continue
            if name not in models:
                models.append(name)

        # Prefer free models first, then the current selection, then the rest.
        preferred: list[str] = []
        current = self.config.model.strip()
        if current:
            preferred.append(current)
        for name in models:
            if name.endswith(":free") and name not in preferred:
                preferred.append(name)
        for name in models:
            if name not in preferred:
                preferred.append(name)

        return preferred or [self.config.model]

    def ask_raw(self, prompt: str) -> str:
        logger.info("Sending raw request to OpenRouter model=%s", self.config.model)
        response = self._post(prompt, stream=False)
        data = response.json()
        return (
            data["choices"][0]["message"]["content"]
            if data.get("choices")
            else ""
        )

    def stream_raw(self, prompt: str) -> Iterator[str]:
        logger.info("Streaming raw request to OpenRouter model=%s", self.config.model)
        response = self._post(prompt, stream=True)

        for line in response.iter_lines(decode_unicode=False):
            if not line:
                continue

            if not line.startswith(b"data: "):
                continue

            payload = line[6:].strip()

            if payload == b"[DONE]":
                break

            try:
                payload_text = payload.decode("utf-8", errors="replace")
                chunk = json.loads(payload_text)
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield content
            except Exception:
                continue

    def ask(self, prompt: str) -> str:
        logger.info("Sending request to OpenRouter model=%s", self.config.model)
        return self.ask_raw(build_context(prompt))

    def stream(self, prompt: str):
        logger.info("Streaming request to OpenRouter model=%s", self.config.model)
        yield from self.stream_raw(build_context(prompt))
