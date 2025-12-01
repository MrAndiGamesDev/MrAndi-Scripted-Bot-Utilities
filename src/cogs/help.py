import random
import discord
from discord.ext import commands
from discord import app_commands
from typing import Dict, List, Optional

try:
    from src.modules.load_config import JsonLoader
except ImportError:
    raise

class HelpPaginator(discord.ui.View):
    """Persistent view for paginating help embeds via text buttons."""

    def __init__(self, chunks: List[List[tuple]], prefix: str, author_id: int):
        super().__init__(timeout=random.randint(60, 120))
        self.chunks = chunks
        self.prefix = prefix
        self.author_id = author_id
        self.current_page = 0
        self.total_pages = len(chunks)
        self._update_buttons()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _update_buttons(self) -> None:
        first = self.current_page <= 0
        last = self.current_page >= self.total_pages - 1
        self.prev_button.disabled = first
        self.prev_buttonx2.disabled = first
        self.next_button.disabled = last
        self.next_buttonx2.disabled = last or self.total_pages < 2

    def _build_embed(self) -> discord.Embed:
        chunk = self.chunks[self.current_page]
        embed = discord.Embed(
            title="🤖 Bot Commands",
            description="Here are the available commands:",
            color=discord.Color.purple(),
        )
        for cmd, desc in chunk:
            embed.add_field(name=f"{self.prefix}{cmd}", value=desc, inline=False)

        footer_lines = [
            f"📜 Page {self.current_page + 1}/{self.total_pages}",
            f"❓ Type {self.prefix}help <command> for details on a specific command.",
            f"❓ Use {self.prefix}help <moderation, fun, utility, admin, owner> to explore command categories.",
        ]
        embed.set_footer(text="\n".join(footer_lines))
        return embed

    # ------------------------------------------------------------------
    # UI callbacks
    # ------------------------------------------------------------------
    @discord.ui.button(label="⏪", style=discord.ButtonStyle.secondary)
    async def prev_buttonx2(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page > 0:
            self.current_page = max(0, self.current_page - 2)
            self._update_buttons()
            await interaction.response.edit_message(embed=self._build_embed(), view=self)

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self._build_embed(), view=self)

    @discord.ui.button(label="⏩", style=discord.ButtonStyle.secondary)
    async def next_buttonx2(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page >= self.total_pages - 1:
            return
        self.current_page = min(self.total_pages - 1, self.current_page + 2)
        self._update_buttons()
        await interaction.response.edit_message(embed=self._build_embed(), view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page >= self.total_pages - 1:
            return
        self.current_page += 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self._build_embed(), view=self)

    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.message.delete()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ You can't control this menu.", ephemeral=True
            )
            return False
        return True

class HelpCog(commands.Cog):
    """Cog that handles the dynamic help command."""

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------
    COMMANDS_INFO: Dict[str, str] = {
        "avatar": "Displays the avatar of a user.",
        "ban": "Bans a member from the server.",
        "botinfo": "Displays information about the bot.",
        "bunny20": "Sends 20 bunny emojis in a single message.",
        "dm": "Make the bot say something in dms.",
        "joke": "Fetches a random meme.",
        "getbadge": "Provides information about getting the Active Developer Badge",
        "giveaway": "Start a giveaway. Duration format: 1d, 2h, 30m (days/hours/minutes).",
        "giveawayreroll": "Reroll the winners of a giveaway.",
        "giveawayend": "End a giveaway.",
        "invite": "Generates and sends an invite link to the server.",
        "kick": "Kicks a member from the server.",
        "level": "Displays the level stats of a user.",
        "addlevel": "Adds levels to a user (Admin only).",
        "removelevel": "Removes levels from a user (Admin only).",
        "lockdown": "Locks/unlocks the channel so that no one/everyone can send messages.",
        "membercount": "Displays the number of members in the server.",
        "meme": "Fetches a random meme.",
        "modmail": "Send/reply to a message to/from the moderators via DM.",
        "note": "Adds a personal note.",
        "notes": "Displays your personal notes.",
        "clearnotes": "Clears all your personal notes.",
        "whomademe": "Displays information about who made the bot.",
        "ping": "Replies with the bot client ping.",
        "purge": "Purges a specified number of messages from the channel.",
        "rps": "Play a game of rock-paper-scissors. Choices: rock, paper, scissors.",
        "replymodmail": "Reply to a message sent to the moderators via DM.",
        "rblxfollowercount": "Fetches the Roblox follower count for a given user ID.",
        "roll": "Rolls a die with a specified number of sides.",
        "say": "Make the bot say something in the specified channel.",
        "setstatus": "Sets the bot's status message.",
        "shutdown": "Shuts down the bot. (Owner only)",
        "serverinfo": "Displays information about the server.",
        "slowmode": "Sets slowmode for the channel in seconds, minutes, or hours.",
        "tempRole": "Assigns a temporary role to a user for a specified duration (e.g., 10m, 1h).",
        "tictactoe": "Play a game of tic-tac-toe with another player.",
        "transactionroblox": "Checks your roblox transactions/robux balances.",
        "unban": "Unbans a member from the server.",
        "uptime": "Shows how long the bot has been online.",
        "clearwarnings": "Clears/warns/displays warnings for a member.",
        "help": "Shows this message",
    }

    CATEGORIES: Dict[str, List[str]] = {
        "moderation": [
            "ban",
            "kick",
            "unban",
            "purge",
            "lockdown",
            "slowmode",
            "clearwarnings",
            "replymodmail",
        ],
        "fun": [
            "joke",
            "rps",
            "bunny20",
            "roll",
            "meme",
            "tictactoe",
        ],
        "utility": [
            "avatar",
            "botinfo",
            "membercount",
            "ping",
            "invite",
            "note",
            "notes",
            "clearnotes",
            "level",
            "addlevel",
            "removelevel",
            "rblxfollowercount",
            "uptime",
            "serverinfo",
        ],
        "admin": [
            "say",
            "dm",
            "giveaway",
            "giveawayreroll",
            "giveawayend",
            "tempRole",
            "modmail",
            "getbadge",
        ],
        "owner": [
            "shutdown",
            "setstatus",
        ],
    }

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    @staticmethod
    def _get_prefix() -> str:
        """Load prefix from config once per invocation."""
        return JsonLoader().load()["Prefix"]

    @staticmethod
    def _chunk_items(items: List[tuple], chunk_size: int = 5) -> List[List[tuple]]:
        """Split a list of tuples into smaller chunks."""
        return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]

    # ------------------------------------------------------------------
    # Embed builders
    # ------------------------------------------------------------------
    def _build_command_embed(self, prefix: str, command: str) -> discord.Embed:
        """Build an embed for a single command."""
        return (
            discord.Embed(
                title=f"📜 Command: {prefix}{command}",
                description=self.COMMANDS_INFO[command],
                color=discord.Color.purple(),
            )
            .set_footer(text=f"Type {prefix}help to see all commands.")
        )

    def _build_category_embed(self, prefix: str, category: str) -> discord.Embed:
        """Build an embed for a category."""
        embed = discord.Embed(
            title=f"📇 Category: {category.capitalize()}",
            description="Here are the commands in this category:",
            color=discord.Color.purple(),
        )
        for cmd in self.CATEGORIES[category]:
            embed.add_field(
                name=f"{prefix}{cmd}",
                value=self.COMMANDS_INFO.get(cmd, "No description available."),
                inline=False,
            )
        embed.set_footer(
            text=f"⌨ Type {prefix}help <command> for details on a specific command."
        )
        return embed

    def _build_not_found_embed(self, prefix: str, query: str) -> discord.Embed:
        """Build an embed for an unknown query."""
        if query.startswith(prefix):
            query = query[len(prefix) :]
        return (
            discord.Embed(
                title="❌ Not Found",
                description=f"No command or category named '{query}' found.",
                color=discord.Color.red(),
            )
            .set_footer(text=f"Type {prefix}help to see all commands.")
        )

    # ------------------------------------------------------------------
    # Slash Commands
    # ------------------------------------------------------------------
    @app_commands.command(name="help", description="Display help for commands and categories.")
    @app_commands.describe(query="Optional command or category name to get specific help")
    async def help_slash(self, interaction: discord.Interaction, query: Optional[str] = None) -> None:
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
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        items = list(self.COMMANDS_INFO.items())
        chunks = self._chunk_items(items)
        total_pages = len(chunks)

        first_embed = HelpPaginator(chunks, prefix, interaction.user.id)._build_embed()
        if total_pages == 1:
            await interaction.response.send_message(embed=first_embed, ephemeral=True)
            return

        view = HelpPaginator(chunks, prefix, interaction.user.id)
        await interaction.response.send_message(embed=first_embed, view=view, ephemeral=True)

    # ------------------------------------------------------------------
    # Legacy text command (optional, remove if not needed)
    # ------------------------------------------------------------------
    @commands.command(name="help", aliases=["commands"])
    async def help_command(self, ctx: commands.Context, *, query: Optional[str] = None) -> None:
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

        items = list(self.COMMANDS_INFO.items())
        chunks = self._chunk_items(items)
        total_pages = len(chunks)

        first_embed = HelpPaginator(chunks, prefix, ctx.author.id)._build_embed()
        if total_pages == 1:
            await ctx.reply(embed=first_embed, mention_author=False)
            return

        view = HelpPaginator(chunks, prefix, ctx.author.id)
        await ctx.reply(embed=first_embed, view=view, mention_author=False)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))