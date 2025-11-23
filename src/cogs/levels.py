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

    @commands.command(name="addlevel", aliases=["addrank"])
    @commands.has_permissions(administrator=True)
    async def addlevel(self, ctx: commands.Context, member: discord.Member, levels: int = 1) -> None:
        """Add levels to a user (admin only)."""
        user = LevelData.get(member.id)
        current_level = user.setdefault("level", 0)
        new_level = current_level + levels

        if new_level < 0:
            await ctx.send("❌ Resulting level must be non-negative.")
            return

        user["level"] = new_level
        user["xp"] = 0
        user["total_xp"] = sum(LevelData.xp_for(lvl) for lvl in range(new_level))
        
        # Persist the updated user data
        LevelData.set(member.id, user)

        embed = discord.Embed(
            title="✅ Levels Added",
            description=f"{member.mention} gained {levels} level(s) and is now **Level {new_level}**.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="removelevel", aliases=["removerank"])
    @commands.has_permissions(administrator=True)
    async def removelevel(self, ctx: commands.Context, member: discord.Member, levels: int = 1) -> None:
        """Remove levels from a user (admin only)."""
        user = LevelData.get(member.id)
        current_level = user.setdefault("level", 0)
        new_level = current_level - levels

        if new_level < 0:
            await ctx.send("❌ Cannot remove more levels than the user currently has.")
            return

        user["level"] = new_level
        user["xp"] = 0
        user["total_xp"] = sum(LevelData.xp_for(lvl) for lvl in range(new_level))
        
        # Persist the updated user data
        LevelData.set(member.id, user)

        embed = discord.Embed(
            title="✅ Levels Removed",
            description=f"{member.mention} lost {levels} level(s) and is now **Level {new_level}**.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Level(bot))