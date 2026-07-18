"""
commands.py
Phantom command framework.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass

from config import APP_NAME, APP_VERSION, SUPPORTED_PROVIDERS
from history import History
from memory import Memory
from runtime import current_settings, set_current_settings, update_current_settings
from settings import (
    PhantomSettings,
    active_model,
    default_model_for,
    provider_key_status,
    provider_label,
    provider_models,
)
from tools import ToolManager


@dataclass
class CommandResult:
    handled: bool
    output: str = ""
    action: str | None = None


class CommandHandler:
    def __init__(
        self,
        memory: Memory | None = None,
        history: History | None = None,
        tools: ToolManager | None = None,
    ):
        self.memory = memory or Memory()
        self.history = history or History()
        self.tools = tools or ToolManager()

    def execute(self, raw_command: str) -> CommandResult:
        command = raw_command.strip()

        if not command.startswith("/"):
            return CommandResult(handled=False)

        try:
            parts = shlex.split(command)
        except ValueError as e:
            return CommandResult(handled=True, output=f"Command parse error: {e}")

        if not parts:
            return CommandResult(handled=True, output="")

        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "/help":
            return CommandResult(handled=True, output=self.help_text())

        if cmd == "/palette":
            return CommandResult(
                handled=True,
                output="Opening the control palette in TUI.",
                action="palette",
            )

        if cmd == "/status":
            return CommandResult(handled=True, output=self.status_text())

        if cmd == "/version":
            return CommandResult(handled=True, output=self.version_text())

        if cmd == "/providers":
            return CommandResult(handled=True, output=self.providers_text())

        if cmd == "/provider":
            return CommandResult(handled=True, output=self.set_provider(args))

        if cmd == "/model":
            return CommandResult(handled=True, output=self.set_model(args))

        if cmd == "/keys":
            return CommandResult(handled=True, output=self.keys_text(args))

        if cmd == "/settings":
            return CommandResult(handled=True, output=self.settings_text())

        if cmd == "/history":
            return CommandResult(handled=True, output=self.history_text())

        if cmd == "/memory":
            return CommandResult(handled=True, output=self.memory_text())

        if cmd == "/remember":
            return CommandResult(handled=True, output=self.remember(args))

        if cmd == "/forget":
            return CommandResult(handled=True, output=self.forget(args))

        if cmd == "/calc":
            result = self.tools.execute("calc", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/time":
            result = self.tools.execute("time", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/file":
            result = self.tools.execute("file", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/read":
            result = self.tools.execute("read", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/write":
            result = self.tools.execute("write", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/append":
            result = self.tools.execute("append", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/mkdir":
            result = self.tools.execute("mkdir", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/rmdir":
            result = self.tools.execute("rmdir", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/pwd":
            result = self.tools.execute("pwd", "")
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/cd":
            result = self.tools.execute("cd", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/home":
            result = self.tools.execute("home", "")
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/cp":
            result = self.tools.execute("copy", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/mv":
            result = self.tools.execute("move", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/rm":
            result = self.tools.execute("remove", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/find":
            result = self.tools.execute("find", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/info":
            result = self.tools.execute("info", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/ls":
            result = self.tools.execute("ls", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/tree":
            result = self.tools.execute("tree", " ".join(args))
            return CommandResult(handled=True, output=result.output or result.error)

        if cmd == "/clear":
            return CommandResult(handled=True, action="clear")

        if cmd == "/exit":
            return CommandResult(handled=True, action="exit")

        return CommandResult(
            handled=True,
            output=f"❓ Unknown command: {cmd}\nType /help for a list of commands.",
        )

    def help_text(self) -> str:
        return (
            "\n📚 Available Commands\n"
            "----------------------\n"
            "/help                       Show commands\n"
            "/palette                    Open the control palette\n"
            "/status                     Show Phantom status\n"
            "/version                    Show Phantom version\n"
            "/providers                  List supported providers\n"
            "/provider [name]            Show or set active provider\n"
            "/model [name]               Show or set active model\n"
            "/keys [provider] [key]      Show or set API key\n"
            "/settings                   Show current runtime settings\n"
            "/history                    Show recent chat history\n"
            "/memory                     Show stored memories\n"
            "/remember <key> <value>     Save a memory\n"
            "/forget <key>               Delete a memory\n"
            "/calc <expression>          Calculate expression\n"
            "/time                       Show current time\n"
            "\n"
            "📁 File Management\n"
            "-------------------\n"
            "/read <file>                Read a file\n"
            "/write <file> <text>        Write text to a file\n"
            "/append <file> <text>       Append text to a file\n"
            "/mkdir <dir>                Create directory\n"
            "/rmdir <dir>                Remove empty directory\n"
            "/pwd                        Show current directory\n"
            "/cd <directory>             Change current directory\n"
            "/home                       Return to workspace root\n"
            "/cp <src> <dst>             Copy file\n"
            "/mv <src> <dst>             Move/Rename file\n"
            "/rm <file>                  Delete file\n"
            "/find <pattern>             Search files\n"
            "/info <file>                Show file information\n"
            "/ls [dir]                   List directory contents\n"
            "/tree [dir]                 Show directory tree\n"
            "\n"
            "⚙️ System\n"
            "--------\n"
            "/file <path>                Show basic file info\n"
            "/clear                      Clear screen\n"
            "/exit                       Exit Phantom\n"
        )

    def status_text(self) -> str:
        settings = current_settings().normalized()
        key_status = provider_key_status(settings)
        models = provider_models(settings)
        memory_count = self.memory.count()
        history_count = self.history.count()
        tools_count = len(self.tools.list_tools())

        return (
            "\n🟢 System Status\n"
            "----------------\n"
            "System : ONLINE\n"
            f"Provider: {provider_label(settings.provider)} ({settings.provider})\n"
            f"Active Model: {settings.model}\n"
            f"Google Model: {models['google']}\n"
            f"OpenRouter Model: {models['openrouter']}\n"
            f"App    : {APP_NAME} {APP_VERSION}\n"
            f"Memory : {memory_count} item(s)\n"
            f"History: {history_count} item(s)\n"
            f"Tools  : {tools_count} available\n"
            f"Keys   : google={'yes' if key_status['google'] else 'missing'}, "
            f"openrouter={'yes' if key_status['openrouter'] else 'missing'}\n"
        )

    def version_text(self) -> str:
        return f"\n🚀 {APP_NAME}\nVersion : {APP_VERSION}\n"

    def providers_text(self) -> str:
        settings = current_settings().normalized()
        key_status = provider_key_status(settings)
        models = provider_models(settings)

        lines = [
            "\n☁ Supported Providers",
            "---------------------",
        ]
        for provider in sorted(SUPPORTED_PROVIDERS):
            current = " (active)" if provider == settings.provider else ""
            keys = "key set" if key_status.get(provider) else "key missing"
            lines.append(
                f"{provider_label(provider)}{current} — {keys} — model: {models.get(provider, default_model_for(provider))}"
            )
        lines.append("")
        return "\n".join(lines)

    def set_provider(self, args: list[str]) -> str:
        settings = current_settings().normalized()

        if not args:
            return (
                f"\nCurrent provider: {provider_label(settings.provider)} ({settings.provider})\n"
                "Usage: /provider <google|openrouter>\n"
            )

        provider = args[0].strip().lower()
        if provider not in SUPPORTED_PROVIDERS:
            return (
                f"\n⚠ Unsupported provider: {provider}\n"
                f"Supported providers: {', '.join(sorted(SUPPORTED_PROVIDERS))}\n"
            )

        saved = set_current_settings(
            PhantomSettings.from_dict(
                {
                    **settings.to_dict(),
                    "provider": provider,
                }
            )
        )
        return (
            f"\n✅ Provider set to {provider_label(saved.provider)} ({saved.provider})\n"
            f"Model: {saved.model}\n"
        )

    def set_model(self, args: list[str]) -> str:
        settings = current_settings().normalized()

        if not args:
            return (
                f"\nCurrent active model: {settings.model}\n"
                f"Google model: {settings.google_model}\n"
                f"OpenRouter model: {settings.openrouter_model}\n"
                "Usage: /model <model-name>\n"
            )

        model = " ".join(args).strip()
        if not model:
            return "\nUsage: /model <model-name>\n"

        changes = settings.to_dict()
        if settings.provider == "google":
            changes["google_model"] = model
        else:
            changes["openrouter_model"] = model
        changes["model"] = model

        saved = set_current_settings(PhantomSettings.from_dict(changes))
        return f"\n✅ Model set to {saved.model}\n"

    def keys_text(self, args: list[str]) -> str:
        settings = current_settings().normalized()

        if not args:
            return (
                "\nUsage: /keys <provider> <api-key>\n"
                "Example: /keys google AIxxxxxxxx\n"
                "Example: /keys openrouter sk-or-v1-xxxxxxxx\n"
            )

        provider = args[0].strip().lower()
        if provider not in SUPPORTED_PROVIDERS:
            return (
                f"\n⚠ Unsupported provider: {provider}\n"
                f"Supported providers: {', '.join(sorted(SUPPORTED_PROVIDERS))}\n"
            )

        if len(args) == 1:
            current_key = settings.google_api_key if provider == "google" else settings.openrouter_api_key
            masked = self._mask_secret(current_key)
            status = "set" if current_key else "missing"
            return (
                f"\n{provider_label(provider)} API key is {status}.\n"
                f"Current: {masked}\n"
                f"Usage: /keys {provider} <api-key>\n"
            )

        api_key = " ".join(args[1:]).strip()
        if not api_key:
            return (
                f"\nUsage: /keys {provider} <api-key>\n"
            )

        clear_value = api_key.lower() in {"clear", "reset", "remove", "delete"}

        changes = settings.to_dict()
        if provider == "google":
            changes["google_api_key"] = "" if clear_value else api_key
        else:
            changes["openrouter_api_key"] = "" if clear_value else api_key

        saved = set_current_settings(PhantomSettings.from_dict(changes))
        current_key = saved.google_api_key if provider == "google" else saved.openrouter_api_key
        action = "cleared" if clear_value else "saved"
        return (
            f"\n✅ {provider_label(provider)} API key {action}.\n"
            f"Current: {self._mask_secret(current_key)}\n"
        )

    def settings_text(self) -> str:
        settings = current_settings().normalized()
        key_status = provider_key_status(settings)
        models = provider_models(settings)

        return (
            "\n⚙ Runtime Settings\n"
            "------------------\n"
            f"Provider : {provider_label(settings.provider)} ({settings.provider})\n"
            f"Active model: {settings.model}\n"
            f"Google model: {models['google']}\n"
            f"OpenRouter model: {models['openrouter']}\n"
            f"Google key: {'set' if key_status['google'] else 'missing'}\n"
            f"OpenRouter key: {'set' if key_status['openrouter'] else 'missing'}\n"
            f"OpenRouter app: {settings.openrouter_app_name}\n"
            f"OpenRouter site: {settings.openrouter_site_url or '(not set)'}\n"
            "\nUse:\n"
            "  /palette\n"
            "  /provider google\n"
            "  /model <name>\n"
            "  /keys google <key>\n"
            "  /keys openrouter <key>\n"
        )

    def history_text(self) -> str:
        items = self.history.last(10)

        if not items:
            return "\n🧠 No conversation history.\n"

        lines = ["\n🧠 Recent Conversation", "--------------------"]

        for item in items:
            lines.append(f'{item["role"]}: {item["message"]}')

        lines.append("")
        return "\n".join(lines)

    def memory_text(self) -> str:
        data = self.memory.all()

        if not data:
            return "\n💾 No stored memories.\n"

        lines = ["\n💾 Stored Memories", "---------------"]

        for key, value in data.items():
            lines.append(f"{key}: {value}")

        lines.append("")
        return "\n".join(lines)

    def remember(self, args: list[str]) -> str:
        if len(args) < 2:
            return "\nUsage: /remember <key> <value>\n"

        key = args[0]
        value = " ".join(args[1:]).strip()

        if not key or not value:
            return "\nUsage: /remember <key> <value>\n"

        self.memory.remember(key, value)
        return f"\n✅ Saved memory: {key} = {value}\n"

    def forget(self, args: list[str]) -> str:
        if len(args) != 1:
            return "\nUsage: /forget <key>\n"

        key = args[0]

        if self.memory.forget(key):
            return f"\n🗑 Deleted memory: {key}\n"

        return f"\n⚠ Memory not found: {key}\n"

    @staticmethod
    def _mask_secret(secret: str) -> str:
        secret = secret.strip()
        if not secret:
            return "(missing)"
        if len(secret) <= 8:
            return "*" * len(secret)
        return f"{secret[:4]}…{secret[-4:]}"
