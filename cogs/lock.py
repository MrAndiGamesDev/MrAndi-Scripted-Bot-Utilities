import discord
from discord.ext import commands

class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)  # Require manage_channels permission
    async def lock_channel(self, ctx):
        """Locks the channel so that no one can send messages."""
        try:
            # Get the current channel
            channel = ctx.channel

            # Modify the channel's permissions to deny the send messages permission for everyone
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)

            # Send a confirmation message
            await ctx.send(f"The channel {channel.mention} has been locked. No one can send messages here.")

        except discord.Forbidden:
            await ctx.send("I don't have permission to edit this channel's settings.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to lock the channel: {e}")

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)  # Require manage_channels permission
    async def unlock_channel(self, ctx):
        """Unlocks the channel so that everyone can send messages again."""
        try:
            # Get the current channel
            channel = ctx.channel

            # Modify the channel's permissions to allow the send messages permission for everyone
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)

            # Send a confirmation message
            await ctx.send(f"The channel {channel.mention} has been unlocked. Everyone can send messages here again.")

        except discord.Forbidden:
            await ctx.send("I don't have permission to edit this channel's settings.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to unlock the channel: {e}")

    @lock_channel.error
    async def lock_error(self, ctx, error):
        """Handles errors related to the lock command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to manage channels.")
        else:
            await ctx.send("An unexpected error occurred while processing the command.")

    @unlock_channel.error
    async def unlock_error(self, ctx, error):
        """Handles errors related to the unlock command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to manage channels.")
        else:
            await ctx.send("An unexpected error occurred while processing the command.")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Lockdown(bot))