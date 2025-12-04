import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="kick", aliases=["kickmember"], help="Kicks a member from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        """Kicks a member from the server."""
        if member == ctx.author:
            await ctx.send("You cannot kick yourself!")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You cannot kick someone with a higher or equal role!")
            return
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ Member Kicked",
                description=f"{member.mention} has been kicked by {ctx.author.mention}",
                color=discord.Color.orange()
            )
            if reason:
                embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick that member!")
        except discord.HTTPException:
            await ctx.send("An error occurred while trying to kick that member.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))