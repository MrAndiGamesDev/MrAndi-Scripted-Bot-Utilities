from discord.ext import commands

class Getbadge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="getbadge", aliases=["badge"])
    async def getbadge(self, ctx: commands.Context):
        """Provides information about getting the Active Developer Badge"""
        messages = [
            "To get the Active Developer Badge, follow this link:",
            "https://discord.com/developers/active-developer"
        ]
        for msg in messages:
            await ctx.send(msg)

async def setup(bot: commands.Bot):
    await bot.add_cog(Getbadge(bot))