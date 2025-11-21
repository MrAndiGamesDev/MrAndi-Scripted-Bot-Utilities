import discord
from discord.ext import commands

class TicTacToe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.games = {}

    @commands.command(name="tictactoe", aliases=["ttt"])
    async def tictactoe(self, ctx: commands.Context, opponent: discord.Member = None):
        if opponent is None or opponent == ctx.author:
            await ctx.send("You need to mention an opponent to play with!")
            return

        if opponent.bot:
            await ctx.send("You can't play against a bot!")
            return

        board = ["⬜"] * 9
        players = [ctx.author, opponent]
        turn = 0

        embed = discord.Embed(
            title="Tic-Tac-Toe",
            description=f"{players[0].mention} vs {players[1].mention}\n\n{self.format_board(board)}",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Turn: {players[turn].display_name}")

        game_message = await ctx.send(embed=embed)

        for i in range(9):
            await game_message.add_reaction(f"{i+1}\u20e3")

        self.games[game_message.id] = {
            "board": board,
            "players": players,
            "turn": turn,
            "message": game_message
        }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if user.bot or reaction.message.id not in self.games:
            return

        game = self.games[reaction.message.id]
        if user not in game["players"] or user != game["players"][game["turn"]]:
            return

        emoji = reaction.emoji
        if emoji not in [f"{i+1}\u20e3" for i in range(9)]:
            return

        index = int(emoji[0]) - 1
        if game["board"][index] != "⬜":
            return

        symbol = "❌" if game["players"].index(user) == 0 else "⭕"
        game["board"][index] = symbol
        game["turn"] = 1 - game["turn"]

        embed = discord.Embed(
            title="Tic-Tac-Toe",
            description=f"{game['players'][0].mention} vs {game['players'][1].mention}\n\n{self.format_board(game['board'])}",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Turn: {game['players'][game['turn']].display_name}")

        await reaction.message.edit(embed=embed)

        winner = self.check_winner(game["board"])
        if winner:
            await reaction.message.channel.send(f"{winner} wins!")
            del self.games[reaction.message.id]
            return

        if "⬜" not in game["board"]:
            await reaction.message.channel.send("It's a draw!")
            del self.games[reaction.message.id]
            return

        await reaction.remove(user)

    def format_board(self, board: list[str]):
        rows = [board[i:i+3] for i in range(0, 9, 3)]
        return "\n".join("".join(row) for row in rows)

    def check_winner(self, board: list[str]):
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for a, b, c in lines:
            if board[a] == board[b] == board[c] and board[a] != "⬜":
                return "❌" if board[a] == "❌" else "⭕"
        return None

async def setup(bot: commands.Bot):
    await bot.add_cog(TicTacToe(bot))