import math
import discord
from discord.ext import commands
from pathlib import Path
from src.events.on_level_event import Level_data

DATA_FILE = Path("src/database/levels.json")

class Level:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="levels", aliases=["lvls"])
    async def levels(self, ctx: commands.Context) -> None:
        user_data = Level_data.get_user_level(ctx.author.id)
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Level Stats",
            description=(
                f"**Level:** {user_data['level']}\n"
                f"**XP:** {user_data['xp']}\n"
                f"**Progress:** {user_data['progress']}/{math.ceil(user_data['level'] * 100)}"
            ),
            color=discord.Color.blue()
        )
        level_message = [":purple_large_square:"]
        for _ in range(user_data['xp']):
            level_message.append(":black_large_square:")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Level(bot))