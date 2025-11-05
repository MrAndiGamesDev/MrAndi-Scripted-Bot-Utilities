import discord
from discord.ext import commands
import aiohttp

class FunCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_meme(self):
        """Fetches a random meme from the API."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as response:
                if response.status == 200:
                    data = await response.json()
                    meme_url = data.get("url", "")
                    if meme_url:
                        return meme_url
                return "Sorry, I couldn't fetch a meme at the moment."

    @commands.command(name="meme")
    async def meme(self, ctx):
        """Fetches a random meme."""
        meme_url = await self.fetch_meme()
        if meme_url and not meme_url.startswith("Sorry"):
            embed = discord.Embed(title="Random Meme", color=discord.Color.blue())
            embed.set_image(url=meme_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't fetch a meme at the moment.")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(FunCommand(bot))