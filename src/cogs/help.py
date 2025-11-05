import discord
from discord.ext import commands
try:
    from src.modules.load_config import load_config
except ImportError:
    # fallback or re-raise as needed
    raise

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        commands_info = {
            "avatar": "Displays the avatar of a user.",
            "ban": "Bans a member from the server.",
            "funCommand": "Fetches a random meme.",
            "getbadge": "Provides information about getting the Active Developer Badge",
            "giveaway": "Start a giveaway. Time is in minutes.",
            "invite": "Generates and sends an invite link to the server.",
            "joke": "Sends a random joke.",
            "kick": "Kicks a member from the server.",
            "lockdown": "Locks/unlocks the channel so that no one/everyone can send messages.",
            "membercount": "Displays the number of members in the server.",
            "modmail": "Send/reply to a message to/from the moderators via DM.",
            "note": "Adds a personal note.",
            "notes": "Displays your personal notes.",
            "clearnotes": "Clears all your personal notes.",
            "ping": "Replies with the bot client ping.",
            "purge": "Purges a specified number of messages from the channel.",
            "rps": "Play a game of rock-paper-scissors. Choices: rock, paper, scissors.",
            "restart": "Restarts the Discord bot.",
            "roll": "Rolls a die with a specified number of sides.",
            "setStatus": "Sets the bot's status message.",
            "shutdown": "Shuts down the bot.",
            "slowmode": "Sets slowmode for the channel in seconds, minutes, or hours.",
            "tempRole": "Assigns a temporary role to a user for a specified duration (e.g., 10m, 1h).",
            "unban": "Unbans a member from the server.",
            "clearwarnings": "Clears/warns/displays warnings for a member.",
            "help": "Shows this message",
        }

        config = load_config()
        prefix = config["Prefix"]

        # Split into chunks of max 25 fields per embed
        chunks = []
        current_chunk = []
        for cmd, desc in commands_info.items():
            current_chunk.append((cmd, desc))
            if len(current_chunk) == 25:
                chunks.append(current_chunk)
                current_chunk = []

        if current_chunk:
            chunks.append(current_chunk)

        # Send first embed
        first_embed = discord.Embed(
            title="Bot Commands",
            description="Here are the available commands:",
            color=discord.Color.purple()
        )
        for cmd, desc in chunks[0]:
            first_embed.add_field(
                name=f"{prefix}{cmd}",
                value=desc,
                inline=False
            )
        first_embed.set_footer(
            text=f"Type {prefix}help command for more info on a command.\n"
                 f"You can also type {prefix}help category for more info on a category."
        )
        await ctx.send(embed=first_embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))