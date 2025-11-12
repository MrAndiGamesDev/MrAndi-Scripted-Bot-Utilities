import discord
from discord.ext import commands
from typing import Dict, List, Optional

try:
    from src.modules.load_config import load_config
except ImportError:
    raise

class HelpCog(commands.Cog):
    """Cog that handles the dynamic help command."""

    COMMANDS_INFO: Dict[str, str] = {
        "avatar": "Displays the avatar of a user.",
        "ban": "Bans a member from the server.",
        "dm": "Make the bot say something in dms.",
        "joke": "Fetches a random meme.",
        "getbadge": "Provides information about getting the Active Developer Badge",
        "giveaway": "Start a giveaway. Time is in minutes.",
        "invite": "Generates and sends an invite link to the server.",
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
        "replymodmail": "Reply to a message sent to the moderators via DM.",
        "restart": "Restarts the Discord bot.",
        "roll": "Rolls a die with a specified number of sides.",
        "say": "Make the bot say something in the specified channel.",
        "setstatus": "Sets the bot's status message.",
        "shutdown": "Shuts down the bot.",
        "slowmode": "Sets slowmode for the channel in seconds, minutes, or hours.",
        "tempRole": "Assigns a temporary role to a user for a specified duration (e.g., 10m, 1h).",
        "unban": "Unbans a member from the server.",
        "clearwarnings": "Clears/warns/displays warnings for a member.",
        "help": "Shows this message",
    }

    CATEGORIES: Dict[str, List[str]] = {
        "moderation": ["ban", "kick", "unban", "purge", "lockdown", "slowmode", "clearwarnings", "replymodmail"],
        "fun": ["joke", "rps", "roll"],
        "utility": ["avatar", "membercount", "ping", "invite", "note", "notes", "clearnotes"],
        "admin": ["restart", "shutdown", "setstatus", "say", "dm", "giveaway", "tempRole", "modmail", "getbadge"],
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def _get_prefix() -> str:
        """Load prefix from config once per invocation."""
        return load_config()["Prefix"]

    @staticmethod
    def _chunk_items(items: List[tuple], chunk_size: int = 5) -> List[List[tuple]]:
        """Split a list of tuples into smaller chunks."""
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

    def _build_command_embed(self, prefix: str, command: str) -> discord.Embed:
        """Build an embed for a single command."""
        return (
            discord.Embed(
                title=f"Command: {prefix}{command}",
                description=self.COMMANDS_INFO[command],
                color=discord.Color.purple()
            )
            .set_footer(text=f"Type {prefix}help to see all commands.")
        )

    def _build_category_embed(self, prefix: str, category: str) -> discord.Embed:
        """Build an embed for a category."""
        embed = discord.Embed(
            title=f"Category: {category.capitalize()}",
            description="Here are the commands in this category:",
            color=discord.Color.purple()
        )
        for cmd in self.CATEGORIES[category]:
            embed.add_field(
                name=f"{prefix}{cmd}",
                value=self.COMMANDS_INFO.get(cmd, "No description available."),
                inline=False
            )
        embed.set_footer(text=f"Type {prefix}help <command> for details on a specific command.")
        return embed

    def _build_not_found_embed(self, prefix: str, query: str) -> discord.Embed:
        """Build an embed for an unknown query."""
        # Strip the prefix from the query if it starts with it
        if query.startswith(prefix):
            query = query[len(prefix):]
        return (
            discord.Embed(
                title="Not Found",
                description=f"No command or category named '{query}' found.",
                color=discord.Color.red()
            )
            .set_footer(text=f"Type {prefix}help to see all commands.")
        )

    def _build_main_help_embed(self, prefix: str, chunk: List[tuple], page: int, total_pages: int) -> discord.Embed:
        """Build the main help embed for a chunk of commands."""
        embed = discord.Embed(
            title="Bot Commands",
            description="Here are the available commands:",
            color=discord.Color.purple()
        )
        for cmd, desc in chunk:
            embed.add_field(name=f"{prefix}{cmd}", value=desc, inline=False)
        embed.set_footer(
            text=f"Page {page}/{total_pages} | Type {prefix}help <command> for details on a specific command.\n"
                 f"Use {prefix}help <moderation, fun, utility, admin> to explore command categories."
        )
        return embed

    @commands.command(name="help", aliases=["commands"])
    async def help_command(self, ctx: commands.Context, *, query: Optional[str] = None):
        """Display help for commands and categories."""
        prefix = self._get_prefix()

        if query:
            query = query.lower()
            if query in self.COMMANDS_INFO:
                embed = self._build_command_embed(prefix, query)
            elif query in self.CATEGORIES:
                embed = self._build_category_embed(prefix, query)
            else:
                embed = self._build_not_found_embed(prefix, query)
            await ctx.reply(embed=embed, mention_author=False)
            return

        # Split commands into chunks and send the first one with pagination
        items = list(self.COMMANDS_INFO.items())
        chunks = self._chunk_items(items)
        total_pages = len(chunks)
        first_embed = self._build_main_help_embed(prefix, chunks[0], 1, total_pages)
        if total_pages == 1:
            await ctx.reply(embed=first_embed, mention_author=False)
            return

        message = await ctx.reply(embed=first_embed, mention_author=False)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]

        current_page = 0
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
            except:
                break
            if str(reaction.emoji) == "➡️":
                if current_page < total_pages - 1:
                    current_page += 1
                    await message.edit(embed=self._build_main_help_embed(prefix, chunks[current_page], current_page + 1, total_pages))
                await message.remove_reaction("➡️", user)
            elif str(reaction.emoji) == "⬅️":
                if current_page > 0:
                    current_page -= 1
                    await message.edit(embed=self._build_main_help_embed(prefix, chunks[current_page], current_page + 1, total_pages))
                await message.remove_reaction("⬅️", user)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))