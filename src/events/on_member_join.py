import discord
from discord.ext import commands

class OnMemberJoined(commands.Cog):
    def __init__(self, bot: commands.Bot, *, channel_id: int) -> None:
        self.bot = bot
        self.channel_id = channel_id

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            channel = self.bot.get_channel(self.channel_id)
            if not channel:
                print("Welcome channel %s not found; skipping message." % self.channel_id)
                return

            embed = (
                discord.Embed(
                    title=f"Welcome {member.display_name}!",
                    description=f"Welcome to {member.guild.name}!",
                    color=discord.Color.purple(),
                    timestamp=discord.utils.utcnow(),
                )
                .set_thumbnail(url=member.display_avatar.url)
            )
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
        
async def setup(bot: commands.Bot):
    await bot.add_cog(OnMemberJoined(bot, channel_id=bot._config["WelcomeAndGoodByeChannel"]))