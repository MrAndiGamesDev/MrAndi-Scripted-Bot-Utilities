import os
import random
import discord
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageDraw
from easy_pil import Canvas, Editor, Font, load_image_async

# Cog that sends a stylized welcome/goodbye card whenever a member joins or leaves the server.
class OnMemberJoinedAndRemoved(commands.Cog):
    # channel_id: ID of the text channel where cards will be posted
    # backgrounds_dir: folder containing PNG/JPG images to randomly pick as card backgrounds
    def __init__(self, bot: commands.Bot, *, channel_id: int, backgrounds_dir: str = "src/assets/icon") -> None:
        self.bot = bot
        self.channel_id = channel_id
        self.backgrounds_dir = backgrounds_dir

    # Retrieve the target text channel, first from cache then via API; returns None if unavailable
    async def _resolve_channel(self) -> discord.TextChannel | None:
        ch = self.bot.get_channel(self.channel_id)
        if ch:
            return ch
        try:
            return await self.bot.fetch_channel(self.channel_id)
        except Exception:
            return None

    # Pick a random background image from self.backgrounds_dir; returns None if folder is empty/missing
    def _pick_background(self) -> str | None:
        if not os.path.isdir(self.backgrounds_dir):
            return None
        files = [f for f in os.listdir(self.backgrounds_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        return os.path.join(self.backgrounds_dir, random.choice(files)) if files else None

    # Build a 1000×300 PNG card: avatar + welcome/goodbye text centered horizontally
    async def _build_card(self, member: discord.Member, *, welcome: bool) -> discord.File:
        # Choose background or fallback to blank canvas
        bg_path = self._pick_background()
        if bg_path:
            background = Editor(Image.open(bg_path).convert("RGBA")).resize((1000, 300))
        else:
            background = Editor(Canvas((1000, 300)))

        # Download and circular-crop member avatar
        avatar = Editor(
            await load_image_async(str(member.display_avatar.url))
        ).resize((150, 150)).circle_image()

        # Font setup
        font_big = Font.poppins(size=35, variant="bold")
        font_small = Font.poppins(size=40, variant="regular")
        text_color = "white"

        # Avatar placement (centered horizontally, 30 px from top)
        avatar_x = (1000 - 150) // 2
        avatar_y = 30

        # Text content
        top_text = f"Welcome {member.display_name}!" if welcome else f"Goodbye {member.display_name}!"
        bottom_text = f"Welcome to {member.guild.name}!" if welcome else f"Left {member.guild.name}!"

        # Measure text widths for horizontal centering
        draw = ImageDraw.Draw(background.image)
        top_bbox = draw.textbbox((0, 0), top_text, font=font_big)
        bottom_bbox = draw.textbbox((0, 0), bottom_text, font=font_small)
        top_w = top_bbox[2] - top_bbox[0]
        bottom_w = bottom_bbox[2] - bottom_bbox[0]

        top_x = (1000 - top_w) // 2
        bottom_x = (1000 - bottom_w) // 2

        # Composite layers: avatar first, then text lines below it
        background.paste(avatar.image, (avatar_x, avatar_y))
        background.text((top_x, avatar_y + 150 + 10), top_text, font=font_big, color=text_color)
        background.text((bottom_x, avatar_y + 150 + 10 + 40 + 10), bottom_text, font=font_small, color=text_color)

        # Export to PNG bytes
        buf = BytesIO()
        background.image.save(buf, format="PNG")
        buf.seek(0)
        return discord.File(fp=buf, filename="card.png")

    # Shorthand for welcome variant
    async def _build_welcome_card(self, member: discord.Member) -> discord.File:
        return await self._build_card(member, welcome=True)

    # Shorthand for goodbye variant
    async def _build_removal_card(self, member: discord.Member) -> discord.File:
        return await self._build_card(member, welcome=False)

    # Event: fires when a new member joins the guild
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        channel = await self._resolve_channel()
        if not channel:
            print(f"Welcome channel {self.channel_id} not found; skipping message.")
            return
        try:
            file = await self._build_welcome_card(member)
            await channel.send(file=file)
        except (discord.Forbidden, discord.HTTPException):
            pass

    # Event: fires when a member leaves the guild
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        channel = await self._resolve_channel()
        if not channel:
            print(f"Removal channel {self.channel_id} not found; skipping message.")
            return
        try:
            file = await self._build_removal_card(member)
            await channel.send(file=file)
        except (discord.Forbidden, discord.HTTPException):
            pass

# Entry point: add this cog to the bot; channel ID is pulled from bot._config
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnMemberJoinedAndRemoved(bot, channel_id=bot._config["WelcomeAndGoodByeChannel"]))