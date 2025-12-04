import random
from discord.ext import commands

try:
    from src.modules.load_config import JsonLoader
except ImportError:
    # fallback or re-raise as needed
    raise

class Joke(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.jsonloader = JsonLoader()
        self.config = self.jsonloader.load()
        self.jokes = self.config["jokes"]

    @commands.command(name="joke", help="Sends a random joke.")
    async def joke(self, ctx: commands.Context):
        """Sends a random joke."""
        joke = random.choice(self.jokes)  # Pick a random joke
        await ctx.send(joke)

# Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(Joke(bot))