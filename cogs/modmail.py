import discord
from discord.ext import commands
import json

with open('config.json') as f:
    config = json.load(f)

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mod_channel_id = config["ModChannelID"]  # Channel ID where moderators will receive messages

    @commands.command(name="modmail")
    async def modmail(self, ctx, *, message: str):
        """Send a message to the moderators via DM."""
        if not message:
            await ctx.send("Please provide a message for the moderators.")
            return

        # Ensure the message is sent from a DM
        if isinstance(ctx.channel, discord.DMChannel):
            embed = discord.Embed(
                title="Modmail",
                description=f"Message from {ctx.author.name}#{ctx.author.discriminator}: {message}",
                color=discord.Color.purple()
            )

            # Send the modmail to the mod channel (defined in config)
            mod_channel = self.bot.get_channel(self.mod_channel_id)

            if mod_channel:
                await mod_channel.send(embed=embed)
                await ctx.send("Your message has been sent to the moderators. They will get back to you shortly.")
            else:
                await ctx.send("Unable to send your message to the moderators. Please try again later.")
        else:
            await ctx.send("This command can only be used in DMs. Please message me in DMs.")

    @commands.command(name="replymodmail")
    @commands.has_permissions(administrator=True)
    async def reply_modmail(self, ctx, user: discord.User, *, reply_message: str):
        """Reply to a user's modmail via DM."""
        if not reply_message:
            await ctx.send("Please provide a reply message.")
            return

        try:
            # Send the reply to the user via DM
            await user.send(f"**Reply from Moderator**: {reply_message}")
            await ctx.send(f"Replied to {user.name}'s modmail.")
        except discord.Forbidden:
            # If the bot cannot DM the user (maybe they have DMs disabled)
            await ctx.send(f"Couldn't send a reply to {user.name}, they may have DMs disabled.")
        except discord.HTTPException as e:
            # In case of any other errors (e.g., message length exceeds limits)
            await ctx.send(f"Failed to send reply: {e}")

    @modmail.error
    async def modmail_error(self, ctx, error):
        """Handles errors that occur in modmail commands."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument. Please provide the necessary information.")
        else:
            await ctx.send("An error occurred while processing your request.")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(ModMail(bot))