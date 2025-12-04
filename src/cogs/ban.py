import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ban", aliases=["banmember"], help="Bans a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        """Bans a member from the server."""
        if member == ctx.author:
            await ctx.send("You cannot ban yourself!")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You cannot ban someone with a higher or equal role!")
            return
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned by {ctx.author.mention}",
                color=discord.Color.red()
            )
            if reason:
                embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban that member!")
        except discord.HTTPException:
            await ctx.send("An error occurred while trying to ban that member.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))