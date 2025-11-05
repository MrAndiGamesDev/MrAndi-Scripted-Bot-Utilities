import datetime
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.gateway import DiscordWebSocket
from dotenv import load_dotenv
from pathlib import Path

try:
    from src.modules.load_config import load_config
    from src.private.set_identify import Mobile
    from src.private.set_identify import PC
except ImportError:
    from modules.load_config import load_config
    from private.set_identify import Mobile
    from private.set_identify import PC

class Bot(commands.Bot):
    def __init__(self, config: dict) -> None:
        self._config = config
        intents = discord.Intents.default()
        intents.message_content = True
        intents.typing = True

        super().__init__(command_prefix=config["Prefix"], intents=intents)
        self.remove_command("help")
        DiscordWebSocket.identify = Mobile.identify

    async def setup_hook(self) -> None:
        await self.load_all_cogs()
        await self.send_status("Bot is now online! 🟢", discord.Color.green())
        
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
        await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f"Need any Help with the bot? Just Use {self._config['Prefix']}help"
                ),
                status=discord.Status.online
            )

    async def load_all_cogs(self) -> None:
        cog_dir = Path(__file__).parent / "src" / "cogs"
        if not cog_dir.exists():
            print(f"Cog directory {cog_dir} not found.")
            return

        for file in cog_dir.glob("*.py"):
            try:
                await self.load_extension(f"src.cogs.{file.stem}")
                print(f"Loaded cog: {file.stem}")
            except Exception as exc:
                print(f"Failed to load cog {file.stem}: {exc}")
                await self.send_status(f"Error loading cog {file.stem}: {exc} ⚠️", discord.Color.orange())

    async def send_status(self, status: str, color: discord.Color) -> None:
        channel = self.get_channel(self._config["StatusChannelID"])
        if channel:
            embed = discord.Embed(
                title="Bot Status Update",
                description=status,
                color=color,
                timestamp=datetime.datetime.now()
            )
            await channel.send(embed=embed)

    async def on_disconnect(self) -> None:
        await self.send_status("Bot has disconnected! 🔴", discord.Color.red())

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"❌ Command not found! Use {self._config["Prefix"]}help to see available commands.")
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