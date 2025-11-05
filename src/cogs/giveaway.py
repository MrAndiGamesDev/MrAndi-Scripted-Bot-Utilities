import discord
from discord.ext import commands
import asyncio
import random

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx, time: int, *, prize: str):
        """Start a giveaway. Time is in minutes."""
        
        # Create embed
        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description="\n".join([
                f"Prize: {prize}",
                "React with 🎉 to enter!",
                f"Time: {time} minutes"
            ]),
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Hosted by {ctx.author.name}")
        
        # Send embed and add reaction
        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")
        
        # Store giveaway info
        self.active_giveaways[message.id] = {
            "prize": prize,
            "host": ctx.author.id,
            "end_time": asyncio.get_event_loop().time() + (time * 60)
        }
        
        # Wait for specified time
        await asyncio.sleep(time * 60)
        
        # Fetch message to get updated reactions
        message = await ctx.channel.fetch_message(message.id)
        
        # Get list of users who reacted (excluding bot)
        users = [user async for user in message.reactions[0].users()]
        users.remove(self.bot.user)
        
        if len(users) == 0:
            await ctx.send("No one entered the giveaway 😔")
            return
            
        # Select winner
        winner = random.choice(users)
        
        # Send winner announcement
        await ctx.send(f"🎉 Congratulations {winner.mention}! You won: **{prize}**!")
        
        # Remove from active giveaways
        del self.active_giveaways[message.id]

async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))