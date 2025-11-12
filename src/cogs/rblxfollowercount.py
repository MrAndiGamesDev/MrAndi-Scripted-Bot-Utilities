import aiohttp
import discord
from discord.ext import commands
from typing import Optional

class RobloxFollowers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roproxy_followers_count_api = "https://friends.roproxy.com/v1/users/{}/followers/count"
        self.roproxy_user_api = "https://users.roproxy.com/v1/users/{}"
        self.roproxy_avatar_api = "https://thumbnails.roproxy.com/v1/users/avatar?userIds={}&size=150x150&format=Png&isCircular=false"

    async def get_follower_count(self, user_id: int) -> Optional[int]:
        try:
            url = self.roproxy_followers_count_api.format(user_id)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Failed to get follower count for user ID {user_id}: {response.status}")
                        return None
                    data = await response.json()
                    return data.get("count")
        except Exception as e:
            print(f"Error getting follower count for user ID {user_id}: {e}")
            return None

    async def get_roblox_avatar_url(self, user_id: int) -> Optional[str]:
        try:
            url = self.roproxy_avatar_api.format(user_id)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    data = await response.json()
                    return data.get("data", [{}])[0].get("imageUrl")
        except Exception as e:
            print(f"Error getting avatar for user ID {user_id}: {e}")
            return None

    async def get_roblox_username(self, user_id: int) -> Optional[str]:
        try:
            url = self.roproxy_user_api.format(user_id)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    data = await response.json()
                    return data.get("name")
        except Exception as e:
            print(f"Error getting username for user ID {user_id}: {e}")
            return None

    @commands.command(name="rblxfollowers", aliases=["rfcount", "rfc"])
    async def followers(self, ctx: commands.Context, user_id: int):
        """Fetch Roblox follower count for a given user ID."""
        try:
            count = await self.get_follower_count(user_id)
            avatar_url = await self.get_roblox_avatar_url(user_id)
            username = await self.get_roblox_username(user_id)
            embed = discord.Embed(
                title="Roblox Follower Count",
                description=(
                    f"User **{username or user_id}** has **{count}** followers."
                    if count is not None
                    else "Could not retrieve follower count for that user."
                ),
                color=discord.Color.green() if count is not None else discord.Color.red()
            )
            embed.set_footer(text="Powered by RoProxy")
            if avatar_url:
                embed.set_thumbnail(url=avatar_url)
            async with ctx.typing():
                await ctx.send(embed=embed)
        except Exception as e:
            error_embed = discord.Embed(
                title="Error",
                description="An error occurred while fetching the follower count.",
                color=discord.Color.red()
            )
            async with ctx.typing():
                await ctx.send(embed=error_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(RobloxFollowers(bot))