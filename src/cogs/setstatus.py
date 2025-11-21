import discord
from discord.ext import commands

class SetStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="setstatus", aliases=["setstat"])
    @commands.is_owner()
    async def setstatus(self, ctx: commands.Context, status_type: str, status_state: str = None, *, status_text: str = None):
        # Map status types to ActivityType
        activity_types = {
            'playing': discord.ActivityType.playing,
            'watching': discord.ActivityType.watching,
            'listening': discord.ActivityType.listening,
            'streaming': discord.ActivityType.streaming
        }
        # Map status states
        status_states = {
            'online': discord.Status.online,
            'idle': discord.Status.idle,
            'dnd': discord.Status.dnd,
            'offline': discord.Status.offline
        }
        # Check if status type is valid
        status_type = status_type.lower()
        if status_type == 'status':
            if not status_state or status_state.lower() not in status_states:
                await ctx.send("❌ Invalid status state! Use 'online', 'idle', 'dnd' or 'offline'")
                return
            try:
                await self.bot.change_presence(status=status_states[status_state.lower()])
                embed = discord.Embed(
                    title="Status Updated",
                    description=f"Bot status state changed to: {status_state.title()}",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                return
            except Exception as e:
                await ctx.send(f"❌ An error occurred: {str(e)}")
                return
        if status_type not in activity_types:
            await ctx.send("❌ Invalid status type! Use 'playing', 'watching', 'listening', 'streaming' or 'status'")
            return
        if not status_text:
            await ctx.send("❌ Please provide status text!")
            return
        try:
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=activity_types[status_type],
                    name=status_text
                )
            )
            embed = discord.Embed(
                title="Status Updated",
                description=f"Bot status changed to: {status_type.title()} {status_text}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.InvalidArgument:
            await ctx.send("❌ Failed to set status: Invalid arguments provided")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

async def setup(bot: commands.Bot):
    await bot.add_cog(SetStatus(bot))