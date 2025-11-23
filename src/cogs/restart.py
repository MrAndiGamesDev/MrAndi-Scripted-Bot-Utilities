import os
import sys
import discord
from discord.ext import commands

class Restart(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="restart", aliases=["reboot"])
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        """Restart the bot."""
        try:
            embed = discord.Embed(
                title="🚀 Restarting bot...",
                description="The bot is restarting now.",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            # On hosting services (Heroku, Railway, etc.) the dyno/container will auto-restart
            # after the process exits, so we simply close the bot gracefully.
            await self.bot.close()
            # On Windows 10 (and local runs) re-launch the same interpreter with the same args
            if sys.platform == "win32":
                # Ensure the script path is quoted to handle spaces
                os.execv(sys.executable, [sys.executable] + [f'"{arg}"' for arg in sys.argv])
            # On Unix-like systems (Linux, macOS) use os.execv as well
            else:
                os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            await ctx.send(f"Failed to restart: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Restart(bot))