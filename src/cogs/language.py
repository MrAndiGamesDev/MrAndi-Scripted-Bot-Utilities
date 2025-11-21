import discord
from discord.ext import commands

class Language(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="whomademe")
    async def whomademe(self, ctx: commands.Context):
        embed = discord.Embed(
            title="🔍 Who Made Me?",
            description="I was made by <@808718935553736714> using a programming language called Python..",
            color=discord.Color.purple(),
        )
        embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-512/free-python-logo-icon-svg-download-png-2945099.png")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Language(bot))