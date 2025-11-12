import discord
from discord.ext import commands
from collections import defaultdict

class WarnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = defaultdict(list)  # Stores warnings in memory

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """Warns a member and records the reason."""
        if member == ctx.author:
            await ctx.send("You cannot warn yourself!")
            return
        if member == ctx.guild.owner:
            await ctx.send("You cannot warn the server owner!")
            return

        self.warnings[member.id].append(reason)
        await ctx.send(f"{member.mention} has been warned for: {reason}")

        # Optionally, DM the user about the warning
        try:
            await member.send(f"You have been warned in **{ctx.guild.name}** for: {reason}")
        except discord.Forbidden:
            await ctx.send(f"Could not DM {member.mention} about their warning.")

    @commands.command(name="warnings")
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        """Displays all warnings for a member."""
        if member.id not in self.warnings or not self.warnings[member.id]:
            await ctx.send(f"{member.mention} has no warnings.")
            return

        embed = discord.Embed(
            title=f"Warnings for {member}",
            color=discord.Color.orange()
        )
        for idx, reason in enumerate(self.warnings[member.id], 1):
            embed.add_field(name=f"Warning {idx}", value=reason, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="clearwarnings", aliases=["clearwarn"])
    @commands.has_permissions(manage_messages=True)
    async def clear_warnings(self, ctx, member: discord.Member):
        """Clears all warnings for a member."""
        if member.id in self.warnings:
            self.warnings[member.id].clear()
        await ctx.send(f"Cleared all warnings for {member.mention}.")

# Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(WarnSystem(bot))