import random
from discord.ext import commands

class RPS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="rps", help="Play a game of rock-paper-scissors. Choices: rock, paper, scissors")
    async def rps(self, ctx: commands.Context, choice: str):
        """Play a game of rock-paper-scissors. Choices: rock, paper, scissors"""
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        choice = choice.lower()

        if choice not in choices:
            embed = discord.Embed(
                title="Invalid Choice",
                description="Please choose rock, paper, or scissors.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if choice == bot_choice:
            result = "It's a tie!"
            color = discord.Color.gold()
        elif (choice == "rock" and bot_choice == "scissors") or \
             (choice == "paper" and bot_choice == "rock") or \
             (choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
            color = discord.Color.green()
        else:
            result = "I win!"
            color = discord.Color.blue()

        embed = discord.Embed(
            title="Rock-Paper-Scissors",
            description=f"{result}",
            color=color
        )
        embed.add_field(name="Your Choice", value=choice.capitalize(), inline=True)
        embed.add_field(name="Bot Choice", value=bot_choice.capitalize(), inline=True)

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(RPS(bot))