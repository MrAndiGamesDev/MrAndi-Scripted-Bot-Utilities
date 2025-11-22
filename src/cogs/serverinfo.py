import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="serverinfo", aliases=["guildinfo"])
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):
        """Display detailed information about the current server."""
        guild = ctx.guild

        embed = discord.Embed(
            title=guild.name,
            description=f"ID: {guild.id}",
            color=discord.Color.purple(),
            timestamp=guild.created_at
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Server overview
        embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="Boost Tier", value=f"Level {guild.premium_tier}", inline=True)

        # Member stats
        total = guild.member_count
        humans = sum(1 for m in guild.members if not m.bot)
        bots = total - humans
        embed.add_field(
            name="Members",
            value=f"{total} total\n{humans} humans\n{bots} bots",
            inline=True
        )

        # Channel counts
        embed.add_field(
            name="Channels",
            value=f"{len(guild.channels)} total\n{len(guild.text_channels)} text\n{len(guild.voice_channels)} voice\n{len(guild.categories)} categories",
            inline=True
        )

        # Role & emoji counts
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Emojis", value=f"{len(guild.emojis)}/{guild.emoji_limit}", inline=True)
        embed.add_field(name="Stickers", value=f"{len(guild.stickers)}/{guild.sticker_limit}", inline=True)

        # Boost info
        embed.add_field(name="Boosters", value=guild.premium_subscription_count, inline=True)
        embed.add_field(name="Filesize Limit", value=f"{guild.filesize_limit // 1024 // 1024} MB", inline=True)
        embed.add_field(name="Max Bitrate", value=f"{guild.bitrate_limit // 1000} kbps", inline=True)

        # Verification & NSFW level
        embed.add_field(name="Verification", value=guild.verification_level.name.title(), inline=True)
        embed.add_field(name="NSFW Level", value=guild.explicit_content_filter.name.replace("_", " ").title(), inline=True)
        embed.add_field(name="Default Notifications", value=guild.default_notifications.name.replace("_", " ").title(), inline=True)

        # Features
        if guild.features:
            embed.add_field(
                name="Features",
                value=", ".join(f.replace("_", " ").title() for f in guild.features[:10]) + (" ..." if len(guild.features) > 10 else ""),
                inline=False
            )

        # Creation date in footer
        created = guild.created_at.strftime("%d %b %Y")
        age = (discord.utils.utcnow() - guild.created_at).days
        embed.set_footer(text=f"Created on {created} • {age} days ago")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfo(bot))