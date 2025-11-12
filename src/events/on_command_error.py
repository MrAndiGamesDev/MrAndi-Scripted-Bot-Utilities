from discord.ext import commands

class OnCommandError(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._config = bot._config

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"❌ Command not found! Use {self._config['Prefix']}help to see available commands.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ You don't have permission to use this command! Use {self._config['Prefix']}help to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument! Please check command usage with {self._config['Prefix']}help.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"❌ Invalid argument provided! Please check command usage with {self._config['Prefix']}help.")
        else:
            await ctx.send(f"❌ An error occurred: {error}")
            print(f"Unhandled error: {error}")

async def setup(bot: commands.Bot):
    await bot.add_cog(OnCommandError(bot))