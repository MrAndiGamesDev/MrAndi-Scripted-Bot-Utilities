import json
import random
import discord
from discord.ext import commands
from pathlib import Path
from typing import Dict, Any
from src.modules.load_config import JsonLoader

PROGRESS_MULTIPLIER = 2
PROGRESS_AMT = 25
XP_AMT = random.randint(3, 8)
DATA_FILE = Path("src/database/levels.json")

class Level_data:
    def __init__(self) -> None:
        pass

    def _load_levels() -> Dict[str, Any]:
        """Load the levels dictionary from disk, returning an empty dict if missing or invalid."""
        try:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_levels(levels: Dict[str, Any]) -> None:
        """Atomically write the levels dictionary to disk."""
        DATA_FILE.write_text(json.dumps(levels, indent=4), encoding="utf-8")

    def get_user_level(user_id: int) -> Dict[str, int]:
        """
        Return the user's level data, creating it if necessary.
        NOTE: Mutations to the returned dict are NOT persisted until save_user_level is called.
        """
        levels = Level_data._load_levels()
        key = str(user_id)
        if key not in levels:
            levels[key] = {"level": 0, "xp": 0, "progress": PROGRESS_AMT}
            Level_data._save_levels(levels)
        return levels[key]

    def save_user_level(user_id: int, data: Dict[str, int]) -> None:
        """Persist the user's level data to disk."""
        levels = Level_data._load_levels()
        levels[str(user_id)] = data
        Level_data._save_levels(levels)

class LevelSystem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.config = JsonLoader("config.json").load()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        user_data = Level_data.get_user_level(message.author.id)
        user_data["progress"] = user_data["progress"]
        user_data["xp"] = user_data["xp"] + XP_AMT

        # Handle multiple level-ups in a single message
        while user_data["xp"] >= user_data["progress"]:
            user_data["level"] = user_data["level"] + 1
            user_data["progress"] = user_data["progress"] * PROGRESS_MULTIPLIER
            user_data["xp"] = 0
            embed = discord.Embed(
                title="🎉 Level Up!",
                description=f"{message.author.mention} has leveled up to level {user_data['level']}!",
                color=discord.Color.purple()
            )
            # Send the level-up embed to the designated channel
            channel = self.bot.get_channel(self.config["LevelChannelID"])
            if channel:
                await channel.send(embed=embed)
            Level_data.save_user_level(message.author.id, user_data)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LevelSystem(bot))