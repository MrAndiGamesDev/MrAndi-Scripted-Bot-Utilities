import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message: str):
        """Make the bot say something in the specified channel."""
        async with channel.typing():
            await channel.send(message)
        await ctx.reply("Message sent!")

async def setup(bot):
    await bot.add_cog(Say(bot))