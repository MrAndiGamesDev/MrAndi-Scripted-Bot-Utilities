import discord
from discord.ext import commands, tasks
import asyncio

class TempRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def temprole(self, ctx, member: discord.Member, role: discord.Role, duration: int):
        """Assigns a temporary role to a user for a specified duration (in seconds)."""
        if member is None or role is None or duration is None:
            await ctx.send("Please specify a member, role, and duration. Usage: `!temprole @member @role duration_in_seconds`")
            return

        await member.add_roles(role)
        await ctx.send(f"Assigned {role.mention} to {member.mention} for {duration} seconds.")
        
        await asyncio.sleep(duration)
        
        await member.remove_roles(role)
        await ctx.send(f"Removed {role.mention} from {member.mention} after {duration} seconds.")

def setup(bot):
    bot.add_cog(TempRole(bot))