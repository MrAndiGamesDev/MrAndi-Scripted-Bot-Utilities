import discord
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, *, member: discord.Member):
        """Unbans a member from the server."""
        try:
            # Get the list of banned users
            banned_users = [entry async for entry in ctx.guild.bans()]
            # Parse the member input (expecting either "name#discriminator" or just "name")
            member_name, member_discriminator = member.split('#') if '#' in member else (member, None)
            # Find the banned user
            banned_member = None
            for ban_entry in banned_users:
                user = ban_entry.user
                if member_discriminator:
                    if user.name == member_name and user.discriminator == member_discriminator:
                        banned_member = user
                        break
                else:
                    if user.name == member_name:
                        banned_member = user
                        break
            if banned_member is None:
                await ctx.send(f"Could not find banned user {member}")
                return
            # Unban the user
            await ctx.guild.unban(banned_member)
            # Create and send embed
            embed = discord.Embed(
                title="✅ Member Unbanned",
                description=f"{banned_member.mention} has been unbanned by {ctx.author.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to unban members!")
        except discord.HTTPException:
            await ctx.send("An error occurred while trying to unban that member.")
        except ValueError:
            await ctx.send("Please provide a valid username or username#discriminator")

async def setup(bot: commands.Bot):
    await bot.add_cog(Unban(bot))