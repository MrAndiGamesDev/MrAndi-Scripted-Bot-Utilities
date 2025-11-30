from discord.ext import commands

class Bunny20(commands.Cog):
    """
    A simple example cog that responds with a bunny emoji and a short message.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="bunny20")
    async def bunny20(self, ctx: commands.Context):
        """
        Sends 20 bunny emojis in a single message.
        Usage: !bunny20
        """
        bunnies = "🐰" * 20
        await ctx.send(bunnies)

async def setup(bot: commands.Bot):
    await bot.add_cog(Bunny20(bot))