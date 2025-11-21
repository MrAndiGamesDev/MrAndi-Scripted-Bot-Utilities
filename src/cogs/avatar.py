import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["ava"])
    async def avatar(self, ctx: commands.Context, user: discord.User = None):
        """Displays the avatar of a user."""
        user = user or ctx.author  # If no user is provided, use the command author's avatar

        # Create an embed to display the avatar
        embed = discord.Embed(
            title=f"{user.name}'s Avatar",
            color=discord.Color.purple()
        )
        embed.set_image(url=user.avatar.url)

        # Send the embed with the avatar
        await ctx.send(embed=embed)

# Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(Avatar(bot))