import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="ping", aliases=["latency"])
    async def ping(self, ctx: commands.Context):  # Changed command name to ping which is more conventional
        PingEmbed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency is {round(self.bot.latency * 1000)}ms",
            color=discord.Color.purple()
        )
        await ctx.send(embed=PingEmbed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))