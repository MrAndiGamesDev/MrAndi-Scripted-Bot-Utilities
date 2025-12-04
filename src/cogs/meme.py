import aiohttp
import os
import discord
from discord.ext import commands

class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tenor_key = os.getenv("TENOR_KEY")  # Replace with your actual Tenor API key
    
    @commands.command(name="meme", help="Fetch a GIF from Tenor based on search query.")
    async def meme(self, ctx: commands.Context, *, search: str = "random"):
        """Fetch a GIF from Tenor based on search query."""
        limit = 20
        url = f"https://g.tenor.com/v1/search?q={search}&key={self.tenor_key}&limit={limit}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("Could not fetch GIF at the moment.")
                data = await resp.json()

        if not data["results"]:
            return await ctx.send("No GIFs found for that search term.")

        gif = data["results"][0]
        gif_url = gif["media"][0]["gif"]["url"]

        embed = discord.Embed(title=f"GIF for: {search}", color=discord.Color.purple())
        embed.set_image(url=gif_url)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))