import discord
from discord.ext import commands

class OnMemberRemoved(commands.Cog):
    def __init__(self, bot: commands.Bot, *, channel_id: int) -> None:
        self.bot = bot
        self.channel_id = channel_id
    
    async def _resolve_channel(self):
        ch = self.bot.get_channel(self.channel_id)
        if ch:
            return ch
        try:
            return await self.bot.fetch_channel(self.channel_id)
        except Exception:
            return None

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            channel = await self._resolve_channel()
            if not channel:
                print("Goodbye channel %s not found; skipping message." % self.channel_id)
                return

            embed = (
                discord.Embed(
                    title=f"Goodbye {member.display_name}!",
                    description=f"Thanks for staying in {member.guild.name}!",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow(),
                )
                .set_thumbnail(url=member.display_avatar.url)
            )
            await channel.send(embed=embed)
        except (discord.Forbidden, discord.HTTPException):
            pass
        
async def setup(bot: commands.Bot):
    await bot.add_cog(OnMemberRemoved(bot, channel_id=bot._config["WelcomeAndGoodByeChannel"]))