import random
import datetime
import discord
from discord.ext import commands
from typing import Dict, List, Optional

# ------------------------------------------------------------------
# Paginator View
# ------------------------------------------------------------------
class UpdateLogPaginator(discord.ui.View):
    """Persistent view for paginating update-log embeds via text buttons."""

    def __init__(self, chunks: List[List[tuple]], author_id: int):
        super().__init__(timeout=random.randint(60, 120))
        self.chunks = chunks
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
            title="📋 Update Logs",
            description="Recent changes and improvements to the bot:",
            color=discord.Color.green(),
        )
        for version, notes in chunk:
            embed.add_field(name=version, value=notes, inline=False)

        footer_lines = [
            f"📜 Page {self.current_page + 1}/{self.total_pages}",
            f"🕒 Last updated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
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

# ------------------------------------------------------------------
# Cog Definition
# ------------------------------------------------------------------
class UpdateLogCog(commands.Cog):
    """Cog that handles the update-log command."""

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------
    UPDATE_LOGS: Dict[str, str] = {
        "v0.1.0": "Initial release with core moderation, fun, utility, admin, and owner commands.",
        "v0.5.5": "Whats New?:\n"
            "Added features: updatelogs.\n"
            "Removed features: leveling system, database system.\n"
            "Refactored a bot utilites.\n"
            "Refactored a bunch of commands and more!.\n"
            "Bugs fixes.\n"
            "And much more!\n"
    }

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    @staticmethod
    def _chunk_items(items: List[tuple], chunk_size: int = 5) -> List[List[tuple]]:
        """Split a list of tuples into smaller chunks."""
        return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]

    # ------------------------------------------------------------------
    # Embed builders
    # ------------------------------------------------------------------
    def _build_version_embed(self, version: str) -> discord.Embed:
        """Build an embed for a single version."""
        return (
            discord.Embed(
                title=f"📦 Version {version}",
                description=self.UPDATE_LOGS[version],
                color=discord.Color.green(),
            )
            .set_footer(text="Use /updatelogs to see the full changelog.")
        )

    def _build_not_found_embed(self, query: str) -> discord.Embed:
        """Build an embed for an unknown version query."""
        return (
            discord.Embed(
                title="❌ Version Not Found",
                description=f"No update log for version '{query}' found.",
                color=discord.Color.red(),
            )
            .set_footer(text="Use /updatelogs to browse all versions.")
        )

    # ------------------------------------------------------------------
    # Legacy text command (optional, remove if not needed)
    # ------------------------------------------------------------------
    @commands.command(name="updatelogs", aliases=["changelog", "updates"], help="Display update logs for the bot.")
    async def updatelogs_command(self, ctx: commands.Context, *, version: Optional[str] = None) -> None:
        """Display update logs for the bot."""
        if version:
            version = version.lower()
            if version in self.UPDATE_LOGS:
                embed = self._build_version_embed(version)
            else:
                embed = self._build_not_found_embed(version)
            await ctx.reply(embed=embed, mention_author=False)
            return

        items = list(self.UPDATE_LOGS.items())
        chunks = self._chunk_items(items)
        total_pages = len(chunks)

        first_embed = UpdateLogPaginator(chunks, ctx.author.id)._build_embed()
        if total_pages == 1:
            await ctx.reply(embed=first_embed, mention_author=False)
            return

        view = UpdateLogPaginator(chunks, ctx.author.id)
        await ctx.reply(embed=first_embed, view=view, mention_author=False)

# ------------------------------------------------------------------
# Cog Setup
# ------------------------------------------------------------------
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UpdateLogCog(bot))