import asyncio
import re
import discord
from discord.ext import commands

class TempRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _parse_duration(self, duration_str: str) -> int:
        """Convert a duration string like '1h30m' or '2d' to seconds."""
        total_seconds = 0
        pattern = re.compile(r'(?P<value>\d+)(?P<unit>[dhms])')
        matches = pattern.findall(duration_str.lower())
        if not matches:
            raise ValueError("Invalid duration format.")
        for value, unit in matches:
            value = int(value)
            if unit == 'd':
                total_seconds += value * 86400
            elif unit == 'h':
                total_seconds += value * 3600
            elif unit == 'm':
                total_seconds += value * 60
            elif unit == 's':
                total_seconds += value
        return total_seconds

    @commands.command(name="temprole", aliases=["temp"])
    @commands.has_permissions(manage_roles=True)
    async def temprole(self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, duration: str):
        """Assigns a temporary role to a user for a specified duration (e.g., 1h30m, 2d, 30s)."""
        if member is None or role is None or duration is None:
            await ctx.send("Please specify a member, role, and duration. Usage: `!temprole @member @role duration`")
            return

        try:
            duration_seconds = self._parse_duration(duration)
        except ValueError:
            await ctx.send("Invalid duration format. Examples: `1h30m`, `2d`, `30s`.")
            return

        await member.add_roles(role)
        await ctx.send(f"Assigned {role.mention} to {member.mention} for {duration}.")

        await asyncio.sleep(duration_seconds)

        await member.remove_roles(role)
        await ctx.send(f"Removed {role.mention} from {member.mention} after {duration}.")

async def setup(bot: commands.Bot):
    await bot.add_cog(TempRole(bot))