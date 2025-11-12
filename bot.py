import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.gateway import DiscordWebSocket
from dotenv import load_dotenv
from pathlib import Path

try:
    from src.modules.load_config import JsonLoader
    from src.modules.set_identify import GetIdentify
except ImportError:
    from modules.load_config import JsonLoader
    from modules.set_identify import GetIdentify

class Bot(commands.Bot):
    def __init__(self, config: dict) -> None:
        self._Is_Mobile = True
        self.jsonloader = JsonLoader()
        self._config = config or self.jsonloader.load()

        intents = discord.Intents.default()
        intents.message_content = True
        intents.typing = True

        super().__init__(command_prefix=config["Prefix"], intents=intents)

        # Remove default help command
        self.remove_command("help")

        # Set identify to mobile by default
        DiscordWebSocket.identify = self.get_identify()

    def get_identify(self) -> GetIdentify:
        return GetIdentify.set_identify_to_mobile if self._Is_Mobile else GetIdentify.set_identify_to_pc

    async def setup_hook(self) -> None:
        # Ensure the client is ready before calling bot events/commands
        await self.load_all_cogs()
        await self.load_all_events()
        # Ensure the client is ready before calling change_presence
        if self.is_ready():
            self.change_presence_status()
        else:
            # Defer change_presence to on_ready if not ready yet
            self.loop.create_task(self._deferred_change_presence())

    async def _deferred_change_presence(self) -> None:
        await self.wait_until_ready()
        await self.change_presence_status()

    async def change_presence_status(self) -> None:
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{self._config['Prefix']}help (If need any help with the bot)"
        )
        await self.change_presence(activity=activity, status=discord.Status.online)

    async def load_all_cogs(self) -> None:
        cog_dir = Path(__file__).parent / "src" / "cogs"
        if not cog_dir.exists():
            print(f"Cog directory {cog_dir} not found.")
            return
        loaded, failed = [], []
        for file in cog_dir.glob("*.py"):
            try:
                await self.load_extension(f"src.cogs.{file.stem}")
                loaded.append(file.stem)
            except Exception as exc:
                failed.append((file.stem, exc))
        for name in loaded:
            print(f"Loaded cog: {name}")
        for name, exc in failed:
            print(f"Failed to load cog {name}: {exc}")

    async def load_all_events(self) -> None:
        event_dir = Path(__file__).parent / "src" / "events"
        if not event_dir.exists():
            print(f"Event directory {event_dir} not found.")
            return
        loaded, failed = [], []
        for file in event_dir.glob("*.py"):
            try:
                await self.load_extension(f"src.events.{file.stem}")
                loaded.append(file.stem)
            except Exception as exc:
                failed.append((file.stem, exc))
        for name in loaded:
            print(f"Loaded event: {name}")
        for name, exc in failed:
            print(f"Failed to load event {name}: {exc}")

class Launcher:
    def __init__(self) -> None:
        load_dotenv()
        self.jsonloader = JsonLoader()
        self.config = self.jsonloader.load()
        self.token = os.getenv("TOKEN")

    def get_token(self) -> str:
        if not self.token:
            raise ValueError("No TOKEN found in environment variables")
        return self.token

    def run(self) -> None:
        bot = Bot(self.config)
        try:
            bot.run(self.get_token())
        except discord.LoginFailure:
            print("Failed to login: Invalid token")
        except Exception as e:
            print(f"Error running bot: {e}")

if __name__ == "__main__":
    BotLauncher = Launcher()
    BotLauncher.run()