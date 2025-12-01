from discord.ext import commands

class Bunny20(commands.Cog):
    """
    A simple example cog that responds with a bunny emoji and a short message.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="bunny20", aliases=["b20"])
    async def bunny20(self, ctx: commands.Context, num: int = None):
        """
        Sends a specified number of bunny emojis in a single message.
        Usage: !bunny20 [num] (default: 1000)
        """
        if num is None:
            await ctx.send("Please provide a number of bunnies to send.")
            return

        bunnies = "🐰" * num
        mention = "<@1385134562652328020>"
        content = f"{mention} {bunnies}"
        for _ in range(num):
            msg = await ctx.send(content)
            await msg.add_reaction("🐰")
            await msg.add_reaction("🐇")
            await msg.add_reaction("🥕")

async def setup(bot: commands.Bot):
    await bot.add_cog(Bunny20(bot))