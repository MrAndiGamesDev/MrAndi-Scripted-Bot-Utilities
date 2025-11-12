import re
import discord
from discord.ext import commands

class Slowmode(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)  # Require manage_channels permission
    async def set_slowmode(self, ctx: commands.Context, time: str):
        """Sets slowmode for the channel in seconds, minutes, or hours."""
        time_in_seconds = self.convert_to_seconds(time)

        if time_in_seconds is None:
            await ctx.send("Invalid time format. Please use `10s`, `5m`, or `2h` (seconds, minutes, or hours).")
            return

        try:
            # Apply the slowmode to the current channel
            await ctx.channel.edit(slowmode_delay=time_in_seconds)
            await ctx.send(f"Slowmode has been set to {time_in_seconds} seconds for this channel.")
        except discord.Forbidden:
            # Bot lacks permissions to modify the channel's settings
            await ctx.send("I don't have permission to edit this channel's settings.")
        except discord.HTTPException as e:
            # Handle other potential errors
            await ctx.send(f"An error occurred while setting slowmode: {e}")
        except Exception as e:
            # Handle other unexpected errors
            await ctx.send(f"An unexpected error occurred: {e}")

    def convert_to_seconds(self, time: str):
        """Convert time in string format (e.g., '10s', '5m', '2h') to seconds."""
        # Regular expression for matching valid time formats (e.g., 10s, 5m, 2h)
        match = re.match(r"^(\d+)([smh])$", time.strip().lower())

        if not match:
            return None

        value = int(match.group(1))  # Extract the numerical value
        unit = match.group(2)        # Extract the unit (s, m, or h)

        # Convert to seconds based on the unit
        if unit == 's':  # Seconds
            return value
        elif unit == 'm':  # Minutes
            return value * 60
        elif unit == 'h':  # Hours
            return value * 3600
        return None

    @set_slowmode.error
    async def slowmode_error(self, ctx: commands.Context, error):
        """Handles errors related to the slowmode command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to manage channels.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the slowmode duration (e.g., `10s`, `5m`, or `2h`).")
        else:
            await ctx.send("An unexpected error occurred while processing the command.")

# Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(Slowmode(bot))