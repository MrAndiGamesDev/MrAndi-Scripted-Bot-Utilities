import asyncio
import random
import re
import discord
from discord.ext import commands

class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_giveaways = {}

    @commands.command(name="giveaway", aliases=["gw"], help="Start a giveaway. Duration format: 1d, 2h, 30m (days/hours/minutes).")
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx: commands.Context, duration: str, *, prize: str):
        """Start a giveaway. Duration format: 1d, 2h, 30m (days/hours/minutes)."""
        
        # Parse duration
        duration_match = re.match(r"(\d+)([dhm])", duration.lower())
        if not duration_match:
            await ctx.send("Invalid duration format! Use: `1d`, `2h`, or `30m` for days/hours/minutes.")
            return
        
        amount, unit = duration_match.groups()
        amount = int(amount)
        
        # Convert to seconds
        if unit == 'd':
            seconds = amount * 86400
            time_str = f"{amount} day{'s' if amount != 1 else ''}"
        elif unit == 'h':
            seconds = amount * 3600
            time_str = f"{amount} hour{'s' if amount != 1 else ''}"
        else:  # 'm'
            seconds = amount * 60
            time_str = f"{amount} minute{'s' if amount != 1 else ''}"
        
        # Cap at 30 days
        if seconds > 2592000:
            await ctx.send("Giveaway duration cannot exceed 30 days!")
            return
        
        # Create embed
        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description="\n".join([
                f"Prize: {prize}",
                "React with 🎉 to enter!",
                f"Duration: {time_str}"
            ]),
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Hosted by {ctx.author.name}")
        
        # Send embed and add reaction
        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")
        
        # Store giveaway info
        self.active_giveaways[message.id] = {
            "prize": prize,
            "host": ctx.author.id,
            "end_time": asyncio.get_event_loop().time() + seconds
        }
        
        # Wait for specified time
        await asyncio.sleep(seconds)
        
        # Fetch message to get updated reactions
        try:
            message = await ctx.channel.fetch_message(message.id)
        except discord.NotFound:
            # Message was deleted, cleanup
            if message.id in self.active_giveaways:
                del self.active_giveaways[message.id]
            return
        
        # Get list of users who reacted (excluding bot)
        users = [user async for user in message.reactions[0].users() if not user.bot]
        
        if len(users) == 0:
            await ctx.send("No one entered the giveaway 😔")
            # Remove from active giveaways
            if message.id in self.active_giveaways:
                del self.active_giveaways[message.id]
            return
            
        # Select winner
        winner = random.choice(users)
        
        # Send winner announcement
        await ctx.send(f"🎉 Congratulations {winner.mention}! You won: **{prize}**!")
        
        # Remove from active giveaways
        if message.id in self.active_giveaways:
            del self.active_giveaways[message.id]

    @commands.command(name="giveawayreroll", aliases=["reroll"], help="Reroll a giveaway winner by message ID.")
    @commands.has_permissions(manage_messages=True)
    async def greroll(self, ctx: commands.Context, message_id: int):
        """Reroll a giveaway winner by message ID."""
        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Message not found!")
            return
        
        # Check if it's a giveaway message
        if not message.embeds or "GIVEAWAY" not in message.embeds[0].title:
            await ctx.send("This doesn't appear to be a giveaway message!")
            return
        
        # Get reactions
        users = [user async for user in message.reactions[0].users() if not user.bot]
        
        if len(users) == 0:
            await ctx.send("No valid entrants to reroll!")
            return
        
        # Select new winner
        winner = random.choice(users)
        
        # Get prize from embed
        prize = message.embeds[0].description.split('\n')[0].replace('Prize: ', '')
        
        await ctx.send(f"🎉 New winner: {winner.mention}! You won: **{prize}**!")

    @commands.command(name="giveawayend", aliases=["gend"], help="End a giveaway early by message ID.")
    @commands.has_permissions(manage_messages=True)
    async def gend(self, ctx: commands.Context, message_id: int):
        """End a giveaway early by message ID."""
        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Message not found!")
            return
        
        # Check if it's an active giveaway
        if message_id not in self.active_giveaways:
            await ctx.send("This giveaway is not active or has already ended!")
            return
        
        # Remove from active giveaways to trigger early end
        del self.active_giveaways[message_id]
        
        await ctx.send("Giveaway ended early!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))