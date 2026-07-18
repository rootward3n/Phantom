"""
providers/google_provider.py

Google AI Studio provider for Phantom.
"""

from __future__ import annotations

from dataclasses import dataclass

from context import build_context
from logger import get_logger

logger = get_logger("phantom.google")


@dataclass(slots=True)
class GoogleProviderConfig:
    model: str
    api_key: str


class GoogleProvider:
    def __init__(
        self,
        *,
        model: str,
        api_key: str,
    ):
        self.config = GoogleProviderConfig(model=model, api_key=api_key)
        self._client = None

    def _ensure_client(self):
        if self._client is not None:
            return self._client

        if not self.config.api_key:
            raise ValueError(
                "Google API key is missing. Open /settings and add GOOGLE_API_KEY."
            )

        try:
            from google import genai
        except Exception as exc:  # pragma: no cover - runtime dependency guard
            raise RuntimeError(
                "google-genai is not installed. Run: pip install google-genai"
            ) from exc

        self._client = genai.Client(api_key=self.config.api_key)
        return self._client

    def _generate_content(self, prompt: str):
        client = self._ensure_client()
        return client.models.generate_content(
            model=self.config.model,
            contents=prompt,
        )

    def _generate_content_stream(self, prompt: str):
        client = self._ensure_client()
        return client.models.generate_content_stream(
            model=self.config.model,
            contents=prompt,
        )


    def list_models(self) -> list[str]:
        """Return available Google models that support text generation."""
        client = self._ensure_client()
        discovered: list[str] = []

        try:
            for model in client.models.list():
                supported = getattr(model, "supported_actions", None) or []
                name = str(getattr(model, "name", "")).strip()
                if not name:
                    continue
                if supported and "generateContent" not in supported:
                    continue
                if name.startswith("models/"):
                    name = name.removeprefix("models/")
                if name not in discovered:
                    discovered.append(name)
        except Exception as exc:  # pragma: no cover - network/runtime guard
            logger.warning("Could not list Google models: %s", exc)
            return [self.config.model]

        if self.config.model and self.config.model not in discovered:
            discovered.insert(0, self.config.model)

        return discovered or [self.config.model]

    def ask_raw(self, prompt: str) -> str:
        logger.info("Sending raw request to Google model=%s", self.config.model)
        response = self._generate_content(prompt)
        return response.text or ""

    def stream_raw(self, prompt: str):
        logger.info("Streaming raw request to Google model=%s", self.config.model)
        stream = self._generate_content_stream(prompt)
        for chunk in stream:
            text = getattr(chunk, "text", None)
            if text:
                yield text

    def ask(self, prompt: str) -> str:
        logger.info("Sending request to Google model=%s", self.config.model)
        return self.ask_raw(build_context(prompt))

    def stream(self, prompt: str):
        logger.info("Streaming request to Google model=%s", self.config.model)
        yield from self.stream_raw(build_context(prompt))
