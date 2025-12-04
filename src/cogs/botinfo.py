import psutil
import pytz
import discord
from discord.ext import commands
from datetime import datetime
from src.modules.load_config import JsonLoader

class BotInfoSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = JsonLoader("config.json").load()
        self.est_tz = pytz.timezone('US/Eastern')

    def _get_system_stats(self) -> dict:
        """Fetch current system statistics."""
        return {
            "cpu": psutil.cpu_percent(),
            "ram_used": psutil.virtual_memory().used / (1024.0 ** 3),
            "ram_total": psutil.virtual_memory().total / (1024.0 ** 3),
            "storage_used": psutil.disk_usage('/').used / (1024.0 ** 3),
            "storage_total": psutil.disk_usage('/').total / (1024.0 ** 3),
        }

    def _build_info_embed(self, ctx: commands.Context, stats: dict) -> discord.Embed:
        """Construct the bot info embed."""
        embed = discord.Embed(
            title=f"{self.bot.user.name}'s Info",
            color=discord.Color.purple()
        )
        created_time_est = self.bot.user.created_at.astimezone(self.est_tz)

        fields = [
            (
                "Bot Info",
                (
                    f"\n**Bot:** {self.bot.user} ({self.bot.user.id})\n"
                    f"**Bot Created At:** {created_time_est.strftime('%a, %d %B %Y, %I:%M %p')} EST\n"
                    f"**Bot CPU Usage:** {stats['cpu']}% / 100%\n"
                    f"**Bot RAM Usage:** {stats['ram_used']:.2f} GB / {stats['ram_total']:.2f} GB\n"
                    f"**Bot Storage Usage:** {stats['storage_used']:.2f} GB / {stats['storage_total']:.2f} GB\n"
                    f"**Bot Ping:** {round(self.bot.latency * 1000)} ms\n"
                    f"**Bot Version:** {self.config['Version']}\n"
                    f"**Bot Library:** discord.py\n"
                    f"**Bot Developer:** mrandi_scripted"
                )
            ),
            (
                "Bot Avatar",
                f"[Click Here to see my avatar!]({self.bot.user.avatar.url})"
            ),
            (
                "Bot Profile",
                f"[Click Here to see my profile!](https://discord.com/users/{self.bot.user.id})"
            )
        ]

        for name, value in fields:
            embed.add_field(
                name=name,
                value=value,
                inline=False
            )

        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(
            text=f'Requested by {ctx.author} at {datetime.now(self.est_tz).strftime("%Y-%m-%d %H:%M:%S %Z")}',
            icon_url=ctx.author.avatar.url
        )
        return embed

    @commands.command(name="botinfo", aliases=["botstats"], help="Displays bot information and system stats.")
    @commands.guild_only()
    async def botinfo(self, ctx: commands.Context):
        try:
            stats = self._get_system_stats()
            embed = self._build_info_embed(ctx, stats)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error sending botinfo command: {e}", color=discord.Color.red()
            )
            print(f'Error sending botinfo message: {e}')
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BotInfoSystem(bot))