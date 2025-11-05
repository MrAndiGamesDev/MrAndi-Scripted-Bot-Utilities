import discord
from discord.ext import commands

class NoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes = {}

    @commands.command()
    async def note(self, ctx, *, content: str):
        """Adds a personal note."""
        if ctx.author.id not in self.notes:
            self.notes[ctx.author.id] = []
        self.notes[ctx.author.id].append(content)
        embed = discord.Embed(
            title="Note Added",
            description=f"**{content}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def notes(self, ctx):
        """Displays your personal notes."""
        if ctx.author.id not in self.notes or not self.notes[ctx.author.id]:
            embed = discord.Embed(
                title="Your Notes",
                description="You have no notes.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            user_notes = self.notes[ctx.author.id]
            notes_list = "\n".join(f"{idx + 1}. {note}" for idx, note in enumerate(user_notes))
            embed = discord.Embed(
                title="Your Notes",
                description=notes_list,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def clearnotes(self, ctx):
        """Clears all your personal notes."""
        self.notes[ctx.author.id] = []
        embed = discord.Embed(
            title="Notes Cleared",
            description="All your notes have been cleared.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(NoteCog(bot))