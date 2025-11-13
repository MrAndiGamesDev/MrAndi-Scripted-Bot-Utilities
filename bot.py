import os
import discord
from discord.ext import commands
from discord.gateway import DiscordWebSocket
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict

try:
    from src.modules.load_config import JsonLoader
    from src.modules.set_identify import GetIdentify
except ImportError:
    from modules.load_config import JsonLoader
    from modules.set_identify import GetIdentify

class Bot(commands.Bot):
    """Refactored bot class with clearer responsibilities and reduced redundancy."""

    def __init__(self, config: Dict) -> None:
        self._is_mobile = True
        self._jsonloader = JsonLoader()
        self._prefix = config.get("Prefix") or self._jsonloader.load().get("Prefix", "!")
        self._config = config

        intents = discord.Intents.default()
        intents.message_content = True
        intents.typing = True

        super().__init__(command_prefix=self._prefix, intents=intents)

        self.remove_command("help")
        DiscordWebSocket.identify = self._get_identify()

    # ---------- internal helpers ----------
    def _get_identify(self):
        return (
            GetIdentify.set_identify_to_mobile
            if self._is_mobile
            else GetIdentify.set_identify_to_pc
        )

    async def _change_presence_once_ready(self) -> None:
        await self.wait_until_ready()
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{self._prefix}help (If need any help with the bot)",
        )
        await self.change_presence(activity=activity, status=discord.Status.online)

    # ---------- public async api ----------
    async def setup_hook(self) -> None:
        base = Path(__file__).parent
        src = base / "src"
        await self._load_extensions(src, src / "cogs")
        await self._load_extensions(src, src / "events")

        # Schedule presence change without blocking startup
        self.loop.create_task(self._change_presence_once_ready())

    async def _load_extensions(self, base: Path, path: Path) -> None:
        if not path.exists():
            print(f"Directory {path} not found – skipped.")
            return

        loaded, failed = [], []
        for file in path.glob("*.py"):
            try:
                await self.load_extension(f"{base.name}.{path.name}.{file.stem}")
                loaded.append(file.stem)
            except Exception as exc:
                failed.append((file.stem, exc))

        for name in loaded:
            print(f"Loaded extension: {name}")
        for name, exc in failed:
            print(f"Failed to load extension {name}: {exc}")

class Launcher:
    """Handles environment setup and bot startup."""

    def __init__(self) -> None:
        load_dotenv()
        self._jsonloader = JsonLoader()
        self._config = self._jsonloader.load()
        self._token = os.getenv("TOKEN")

    def _validate_token(self) -> str:
        if not self._token:
            raise ValueError("No TOKEN found in environment variables")
        return self._token

    def run(self) -> None:
        bot = Bot(self._config)
        try:
            bot.run(self._validate_token())
        except discord.LoginFailure:
            print("Failed to login: Invalid token")
        except Exception as e:
            print(f"Error running bot: {e}")

if __name__ == "__main__":
    BotLauncher = Launcher()
    BotLauncher.run()