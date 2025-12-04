import os
import discord
from discord.ext import commands
from discord.gateway import DiscordWebSocket
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, List, Callable, Tuple, Optional

try:
    from src.modules.load_config import JsonLoader
    from src.modules.set_identify import GetIdentify
except ImportError:
    from modules.load_config import JsonLoader
    from modules.set_identify import GetIdentify

class Bot(commands.Bot):
    """Refactored bot class with clearer responsibilities and reduced redundancy."""

    def __init__(self, config: Dict) -> Any:
        self._is_mobile: bool = True
        self._jsonloader: JsonLoader = JsonLoader()
        self._prefix: str = config.get("Prefix") or self._jsonloader.load().get("Prefix")
        self._config: Dict[str, Any] = config

        self._intents: discord.Intents = discord.Intents.default()
        self._intents.message_content: bool = True
        self._intents.typing: bool = True
        self._intents.presences: bool = True
        self._intents.members: bool = True

        super().__init__(command_prefix=self._prefix, intents=self._intents)

        self.remove_command("help")
        DiscordWebSocket.identify: Callable[[], Dict[str, Any]] = self._get_identify()

    # ---------- internal helpers ----------
    def _get_identify(self) -> bool:
        return (
            GetIdentify.set_identify_to_mobile
            if self._is_mobile
            else GetIdentify.set_identify_to_pc
        )

    # ---------- public async api ----------
    async def setup_hook(self) -> Any:
        base: Path = Path(__file__).parent
        src: Path = base / "src"
        await self._load_extensions(src, src / "cogs")
        await self._load_extensions(src, src / "events")

        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} slash command(s)")
        except Exception as e:
            print(f"Failed to sync slash commands: {e}")

    async def _load_extensions(self, base: Path, path: Path) -> Optional[str]:
        if not path.exists():
            print(f"Directory {path} not found – skipped.")
            return None

        loaded: List[str] = []
        failed: List[Tuple[str, Exception]] = []

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

    def __init__(self) -> Any:
        load_dotenv()
        
        self._jsonloader: JsonLoader = JsonLoader()
        self._config: Dict[str, Any] = self._jsonloader.load()
        self._token: str | None = os.getenv("TOKEN")

    def _validate_token(self) -> bool:
        if not self._token:
            raise ValueError("No TOKEN found in environment variables")
        return self._token

    def run(self) -> Any:
        bot: Bot = Bot(self._config)
        try:
            bot.run(self._validate_token())
        except discord.LoginFailure:
            print("Failed to login: Invalid token")
        except Exception as e:
            print(f"Error running bot: {e}")

if __name__ == "__main__":
    bot_launcher = Launcher()
    bot_launcher.run()