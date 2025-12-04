import datetime
import discord
from discord.ext import commands

class Uptime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.datetime.now(datetime.timezone.utc)

    @commands.command(name="uptime", help="Displays the bot's uptime.", aliases=["up"])
    async def uptime(self, ctx: commands.Context):
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        embed = discord.Embed(
            title="⏰ Bot Uptime",
            description=f"i've have been online for **{uptime_str}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Uptime(bot))