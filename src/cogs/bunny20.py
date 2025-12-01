from discord.ext import commands

class Bunny20(commands.Cog):
    """
    A simple example cog that responds with a bunny emoji and a short message.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.msg = None

    @commands.command(name="bunny20")
    async def bunny20(self, ctx: commands.Context):
        """
        Sends 20 bunny emojis in a single message.
        Usage: !bunny20
        """
        maxnum = 20
        bunnies = "🐰" * maxnum
        self.msg = None
        mention = "<@1385134562652328020>"
        content = f"{mention} {bunnies}"
        for _ in range(maxnum):
            self.msg = await ctx.send(content)
        await self.msg.add_reaction("🐰")
        await self.msg.add_reaction("🐇")

async def setup(bot: commands.Bot):
    await bot.add_cog(Bunny20(bot))