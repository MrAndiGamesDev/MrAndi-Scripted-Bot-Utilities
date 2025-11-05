import os
import sys
import discord
from discord.ext import commands

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart", aliases=["reboot"])
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot."""
        embed = discord.Embed(
            title="Restarting bot...",
            description="The bot is restarting now.",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        # Schedule the actual restart after the message is sent
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(Restart(bot))