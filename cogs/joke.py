import discord
from discord.ext import commands
import random
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jokes = config["jokes"]

    @commands.command(name="joke")
    async def joke(self, ctx):
        """Sends a random joke."""
        joke = random.choice(self.jokes)  # Pick a random joke
        await ctx.send(joke)

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Joke(bot))