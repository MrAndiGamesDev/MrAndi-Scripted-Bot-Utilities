import discord
from discord.ext import commands
from easy_pil import Canvas, Editor, Font, load_image_async

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

            # Create image with easy_pil
            background = Editor(Canvas((1000, 300), color="#6b00bc"))
            avatar = await load_image_async(str(member.display_avatar.url))
            avatar = Editor(avatar).resize((150, 150)).circle_image()

            # Fonts
            font_big = Font.poppins(size=35, variant="bold")
            font_small = Font.poppins(size=40, variant="regular")
            text_color = "white"

            # Paste avatar
            background.paste(avatar.image, (50, 50))

            # Write text
            background.text(
                (280, 50),
                f"Goodbye {member.display_name}!",
                font=font_big,
                color=text_color
            )

            background.text(
                (215, 200),
                f"Thanks for staying in {member.guild.name}!",
                font=font_small,
                color=text_color
            )
            
            assets = "src/assets"
            file = discord.File(fp=background.image_bytes, filename=f"{assets}/pic.png")

            await channel.send(file=file)
        except (discord.Forbidden, discord.HTTPException):
            pass
        
async def setup(bot: commands.Bot):
    await bot.add_cog(OnMemberRemoved(bot, channel_id=bot._config["WelcomeAndGoodByeChannel"]))