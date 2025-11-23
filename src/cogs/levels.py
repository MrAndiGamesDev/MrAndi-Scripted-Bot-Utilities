import discord
from discord.ext import commands
from src.modules.load_config import JsonLoader
from src.events.on_level_event import LevelData

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = JsonLoader("config.json").load()

    @commands.command(name="level", aliases=["rank"])
    async def rank(self, ctx: commands.Context, member: discord.Member = None) -> None:
        """Check your or another member's level and XP."""
        target = member or ctx.author
        user = LevelData.get(target.id)
        user.setdefault("total_xp", 0)
        user.setdefault("xp", 0)
        user.setdefault("level", 0)

        needed = LevelData.xp_for(user["level"])
        bar = LevelData.progress_bar(user["xp"], needed)

        embed = discord.Embed(
            title=f"{target.display_name}'s Level",
            description=(
                f"**Level {user['level']}**\n"
                f"`{bar}` {user['xp']} / {needed} XP\n"
                f"Total XP: {user['total_xp']}"
            ),
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="setlevel", aliases=["setrank"])
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx: commands.Context, member: discord.Member, new_level: int) -> None:
        """Set a user's level (admin only)."""
        if new_level < 0:
            await ctx.send("❌ Level must be non-negative.")
            return

        user = LevelData.get(member.id)
        user["level"] = new_level
        user["xp"] = 0
        user["total_xp"] = LevelData.total_xp_for(new_level)
        
        LevelData.save(member.id, user)

        embed = discord.Embed(
            title="✅ Level Updated",
            description=f"{member.mention} is now **Level {new_level}**.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Level(bot))