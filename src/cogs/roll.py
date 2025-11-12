import random
import discord
from discord.ext import commands

class Roll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context, sides: int):
        if sides < 1:
            await ctx.send("Please provide a number greater than 0.")
            return
        result = random.randint(1, sides)
        RollEmbed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"{ctx.author.mention} rolled a {result} on a {sides}-sided dice!",
            color=discord.Color.purple()
        )
        await ctx.send(embed=RollEmbed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Roll(bot))