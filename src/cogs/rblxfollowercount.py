import asyncio
import time
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
        self.roblox_followers_count_api = "https://friends.roblox.com/v1/users/{}/followers/count"
        self.roblox_user_api = "https://users.roblox.com/v1/users/{}"
        self.roblox_avatar_api = "https://thumbnails.roblox.com/v1/users/avatar?userIds={}&size=150x150&format=Png&isCircular=false"
        self.timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        self.cache = {}

    async def cog_unload(self):
        await self.session.close()

    async def _fetch_json(self, url: str, retries: int = 3) -> Optional[dict]:
        for attempt in range(retries):
            try:
                async with self.session.get(url) as response:
                    if response.status == 429:
                        retry_after = response.headers.get("Retry-After")
                        delay = float(retry_after) if retry_after else 1.0 * (2 ** attempt)
                        await asyncio.sleep(delay)
                        continue
                    if 200 <= response.status < 300:
                        return await response.json()
                    if 500 <= response.status < 600:
                        await asyncio.sleep(1.0 * (2 ** attempt))
                        continue
                    return None
            except (aiohttp.ClientError, asyncio.TimeoutError):
                await asyncio.sleep(1.0 * (2 ** attempt))
            except Exception as e:
                print(f"Request failure: {e}")
                return None
        return None

    async def get_follower_count(self, user_id: int) -> Optional[int]:
        cache_key = f"count:{user_id}"
        cached = self.cache.get(cache_key)
        if cached and time.monotonic() - cached.get("ts", 0) < 60:
            return cached.get("value")
        data = await self._fetch_json(self.roproxy_followers_count_api.format(user_id))
        if not data:
            data = await self._fetch_json(self.roblox_followers_count_api.format(user_id))
        if not data:
            return None
        value = data.get("count")
        self.cache[cache_key] = {"value": value, "ts": time.monotonic()}
        return value

    async def get_roblox_avatar_url(self, user_id: int) -> Optional[str]:
        cache_key = f"avatar:{user_id}"
        cached = self.cache.get(cache_key)
        if cached and time.monotonic() - cached.get("ts", 0) < 300:
            return cached.get("value")
        data = await self._fetch_json(self.roproxy_avatar_api.format(user_id))
        if not data:
            data = await self._fetch_json(self.roblox_avatar_api.format(user_id))
        if not data:
            return None
        image_url = None
        try:
            arr = data.get("data")
            if isinstance(arr, list) and arr:
                image_url = arr[0].get("imageUrl")
        except Exception:
            image_url = None
        if image_url:
            self.cache[cache_key] = {"value": image_url, "ts": time.monotonic()}
        return image_url

    async def get_roblox_username(self, user_id: int) -> Optional[str]:
        cache_key = f"username:{user_id}"
        cached = self.cache.get(cache_key)
        if cached and time.monotonic() - cached.get("ts", 0) < 300:
            return cached.get("value")
        data = await self._fetch_json(self.roproxy_user_api.format(user_id))
        if not data:
            data = await self._fetch_json(self.roblox_user_api.format(user_id))
        if not data:
            return None
        name = data.get("name")
        if name:
            self.cache[cache_key] = {"value": name, "ts": time.monotonic()}
        return name

    @commands.command(name="rblxfollowers", help="Displays the Roblox follower count for the specified user ID.", aliases=["rfcount", "rfc"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def followers(self, ctx: commands.Context, user_id: int):
        try:
            async with ctx.typing():
                count_task = self.get_follower_count(user_id)
                avatar_task = self.get_roblox_avatar_url(user_id)
                username_task = self.get_roblox_username(user_id)
                count, avatar_url, username = await asyncio.gather(count_task, avatar_task, username_task)
            title = "Roblox Follower Count"
            if count is not None:
                desc = f"User **{username or user_id}** has **{count}** followers.\nhttps://www.roblox.com/users/{user_id}/profile"
                color = discord.Color.green()
            else:
                desc = "Could not retrieve follower count for that user."
                color = discord.Color.red()
            embed = discord.Embed(title=title, description=desc, color=color)
            embed.set_footer(text="Powered by RoProxy/Roblox API")
            if avatar_url:
                embed.set_thumbnail(url=avatar_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Command error: {e}")
            error_embed = discord.Embed(title="Error", description="An error occurred while fetching the follower count.", color=discord.Color.red())
            await ctx.send(embed=error_embed)

    @followers.error
    async def followers_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Try again in {round(error.retry_after, 1)}s.")

async def setup(bot: commands.Bot):
    await bot.add_cog(RobloxFollowers(bot))