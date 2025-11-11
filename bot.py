import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.gateway import DiscordWebSocket
from dotenv import load_dotenv
from pathlib import Path

try:
    from src.modules.load_config import load_config
    from src.private.set_identify import Mobile, PC
except ImportError:
    from modules.load_config import load_config
    from private.set_identify import Mobile, PC

class Bot(commands.Bot):
    def __init__(self, config: dict) -> None:
        self._Is_Mobile = True
        self._config = config or load_config()
        intents = discord.Intents.default()
        intents.message_content = True
        intents.typing = True

        super().__init__(command_prefix=config["Prefix"], intents=intents)
        self.remove_command("help")
        DiscordWebSocket.identify = self.IsMobile()

    def IsMobile(self) -> bool:
        if self._Is_Mobile == True:
            return Mobile.identify
        return PC.identify

    async def setup_hook(self) -> None:
        await self.load_all_cogs()
        
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
            name=f"Need any Help with the bot? Just Use {self._config['Prefix']}help"
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

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"❌ Command not found! Use {self._config['Prefix']}help to see available commands.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ You don't have permission to use this command! Use {self._config['Prefix']}help to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument! Please check command usage with {self._config['Prefix']}help.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"❌ Invalid argument provided! Please check command usage with {self._config['Prefix']}help.")
        else:
            await ctx.send(f"❌ An error occurred: {error}")
            print(f"Unhandled error: {error}")

class BotStarter:
    def __init__(self) -> None:
        load_dotenv()
        self.config = load_config()
        self.token = os.getenv("TOKEN")
        if not self.token:
            raise ValueError("No TOKEN found in environment variables")

    def run(self) -> None:
        bot = Bot(self.config)
        try:
            bot.run(self.token)
        except discord.LoginFailure:
            print("Failed to login: Invalid token")
        except Exception as e:
            print(f"Error running bot: {e}")

if __name__ == "__main__":
    BotLauncher = BotStarter()
    BotLauncher.run()