import discord
from discord.ext import commands

class DMCog(commands.Cog):
    """Cog for sending direct messages to users."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="dm")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx: commands.Context, member: discord.Member, *, message: str):
        """Send a direct message to a specified user."""
        try:
            await member.send(message)
            await ctx.send(f"✅ DM sent to {member.mention}.")
        except discord.Forbidden:
            await ctx.send("❌ I can't DM that user. They may have DMs disabled or blocked the bot.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to send DM: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(DMCog(bot))