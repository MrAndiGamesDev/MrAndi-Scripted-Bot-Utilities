import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="Bot Commands",
            description="Here are the available commands:",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="!Avatar: ",
            value="Displays the avatar of a user.",
            inline=False
        )
        embed.add_field(
            name="!Ban: ",
            value="Bans a member from the server.",
            inline=False
        )
        embed.add_field(
            name="!FunCommand: ",
            value="Fetches a random meme.",
            inline=False
        )
        embed.add_field(
            name="!Getbadge: ",
            value="Provides information about getting the Active Developer Badge",
            inline=False
        )
        embed.add_field(
            name="!Giveaway: ",
            value="Start a giveaway. Time is in minutes.",
            inline=False
        )
        embed.add_field(
            name="!Invite: ",
            value="Generates and sends an invite link to the server.",
            inline=False
        )
        embed.add_field(
            name="!Joke: ",
            value="Sends a random joke.",
            inline=False
        )
        embed.add_field(
            name="!Kick: ",
            value="Kicks a member from the server.",
            inline=False
        )
        embed.add_field(
            name="!Lockdown: ",
            value="Locks the channel so that no one can send messages.\n"
                  "Unlocks the channel so that everyone can send messages again.",
            inline=False
        )
        embed.add_field(
            name="!MemberCount: ",
            value="Displays the number of members in the server.",
            inline=False
        )
        embed.add_field(
            name="!ModMail: ",
            value="Send a message to the moderators via DM.\n"
                  "Reply to a user's modmail via DM.",
            inline=False
        )
        embed.add_field(
            name="!NoteCog: ",
            value="Clears all your personal notes.\n"
                  "Adds a personal note.\n"
                  "Displays your personal notes.",
            inline=False
        )
        embed.add_field(
            name="!Ping: ",
            value="Replys with a bot client pings",
            inline=False
        )
        embed.add_field(
            name="!Purge: ",
            value="Purges a specified number of messages from the channel.",
            inline=False
        )
        embed.add_field(
            name="!RPS: ",
            value="Play a game of rock-paper-scissors. Choices: rock, paper, sci...",
            inline=False
        )
        embed.add_field(
            name="!Restart: ",
            value="Restarts the discord bot.",
            inline=False
        )
        embed.add_field(
            name="!Roll: ",
            value="Rolls a die with a specified number of sides.",
            inline=False
        )
        embed.add_field(
            name="!SetStatus: ",
            value="Sets the bot's status message.",
            inline=False
        )
        embed.add_field(
            name="!Shutdown: ",
            value="Shuts down the bot.",
            inline=False
        )
        embed.add_field(
            name="!Slowmode: ",
            value="Sets slowmode for the channel in seconds, minutes, or hours.",
            inline=False
        )
        embed.add_field(
            name="!TempRole: ",
            value="Assigns a temporary role to a user for a specified duration (e.g., 10m, 1h).",
            inline=False
        )
        embed.add_field(
            name="!Unban: ",
            value="Unbans a member from the server.",
            inline=False
        )
        embed.add_field(
            name="!WarnSystem: ",
            value="Clears all warnings for a member.\n"
                  "Warns a member and records the reason.\n"
                  "Displays all warnings for a member.",
            inline=False
        )
        embed.add_field(
            name="​!No Category: ",
            value="!help Shows this message",
            inline=False
        )
        embed.set_footer(
            text="Type !help command for more info on a command.\n"
                 "You can also type !help category for more info on a category."
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
