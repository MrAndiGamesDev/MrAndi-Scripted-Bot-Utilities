import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="purge", help="Purges a specified number of messages from the channel.", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int):
        """Purges a specified number of messages from the channel."""
        if amount <= 0:
            await ctx.send("Please specify a positive number of messages to delete!")
            return
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
            embed = discord.Embed(
                title="Messages Purged",
                description=f"Successfully deleted {len(deleted)-1} messages.",
                color=discord.Color.purple()
            )
            confirmation = await ctx.send(embed=embed)
            await confirmation.delete(delay=5)  # Delete confirmation after 5 seconds
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages!")
        except discord.HTTPException:
            await ctx.send("An error occurred while trying to delete messages.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Purge(bot))