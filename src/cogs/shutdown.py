import discord
from discord.ext import commands

class Shutdown(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Shutting Down",
            description="The bot is going offline...",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await self.bot.close()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Shutdown(bot))