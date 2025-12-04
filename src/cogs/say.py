import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="say", help="Makes the bot say something in the specified channel.", aliases=["echo"])
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message: str):
        """Make the bot say something in the specified channel."""
        async with channel.typing():
            await channel.send(message)
        await ctx.reply("✅ Message sent!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))