import os
import signal
import discord
from discord.ext import commands

class Shutdown(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name="shutdown", aliases=["die"])
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="🚫 Shutting Down",
            description="I am going offline so bye bye now!",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await self.bot.close()
        # Forcefully terminate the entire Python process
        os.kill(os.getpid(), signal.SIGTERM)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Shutdown(bot))