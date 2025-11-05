import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def invite(self, ctx):
        """Generates and sends an invite link to the server."""
        try:
            # Check if the bot has permission to create invites
            if not ctx.guild.me.guild_permissions.create_instant_invite:
                embed = discord.Embed(
                    title="Permission Denied",
                    description="I don't have permission to create an invite link. Please check my permissions.",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=embed)

            # Check if the user has permission to generate an invite
            if not ctx.author.guild_permissions.manage_guild:
                embed = discord.Embed(
                    title="Permission Denied",
                    description="You do not have permission to generate an invite link.",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=embed)

            # Create a server invite with no expiration and unlimited uses
            invite = await ctx.channel.create_invite(
                max_age=0, max_uses=0  # Never expire, infinite uses
            )
            embed = discord.Embed(
                title="Server Invite",
                description=f"[Click here to join the server]({invite.url})",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="Permission Denied",
                description="I don't have permission to create an invite link. Please check my permissions.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="HTTP Error",
                description=f"An error occurred while creating the invite link: {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Unexpected Error",
                description=f"An unexpected error occurred: {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

# Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(Invite(bot))