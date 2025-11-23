import sqlite3
import random
import discord
from discord.ext import commands
from pathlib import Path
from typing import Dict, Any
from src.modules.load_config import JsonLoader

DB_FILE = Path("src/database/levels.db")
XP_RANGE = (3, 8)
BASE_XP = 100
XP_MULTIPLIER = 1.5
PROGRESS_BAR_LENGTH = 20
PROGRESS_FILLED = "█"
PROGRESS_EMPTY = "░"

class LevelData:
    @staticmethod
    def _init_db() -> None:
        with sqlite3.connect(DB_FILE) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS levels (
                    user_id INTEGER PRIMARY KEY,
                    level INTEGER DEFAULT 0,
                    xp INTEGER DEFAULT 0,
                    total_xp INTEGER DEFAULT 0
                )
            """)
            db.commit()

    @staticmethod
    def get(user_id: int) -> Dict[str, Any]:
        LevelData._init_db()
        with sqlite3.connect(DB_FILE) as db:
            cursor = db.execute("SELECT level, xp, total_xp FROM levels WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row is None:
                db.execute("INSERT INTO levels (user_id) VALUES (?)", (user_id,))
                db.commit()
                return {"level": 0, "xp": 0, "total_xp": 0}
            return {"level": row[0], "xp": row[1], "total_xp": row[2]}

    @staticmethod
    def set(user_id: int, payload: Dict[str, Any]) -> None:
        LevelData._init_db()
        with sqlite3.connect(DB_FILE) as db:
            db.execute(
                "INSERT OR REPLACE INTO levels (user_id, level, xp, total_xp) VALUES (?, ?, ?, ?)",
                (user_id, payload["level"], payload["xp"], payload["total_xp"])
            )
            db.commit()

    @staticmethod
    def xp_for(level: int) -> int:
        return int(BASE_XP * (XP_MULTIPLIER ** level))

    @staticmethod
    def progress_bar(current: int, needed: int) -> str:
        ratio = max(0, min(1, current / needed))
        filled = int(PROGRESS_BAR_LENGTH * ratio)
        return PROGRESS_FILLED * filled + PROGRESS_EMPTY * (PROGRESS_BAR_LENGTH - filled)

class LevelSystem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = JsonLoader("config.json").load()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        user = LevelData.get(message.author.id)
        
        # Ensure all required keys exist
        user.setdefault("total_xp", 0)
        user.setdefault("xp", 0)
        user.setdefault("level", 0)

        gained = random.randint(*XP_RANGE)
        user["total_xp"] += gained
        user["xp"] += gained

        while True:
            needed = LevelData.xp_for(user["level"])
            if user["xp"] < needed:
                break
            user["xp"] -= needed
            user["level"] += 1
            bar = LevelData.progress_bar(0, LevelData.xp_for(user["level"]))
            embed = discord.Embed(
                title="🎉 Level Up!",
                description=(
                    f"{message.author.mention} reached **Level {user['level']}**!\n"
                    f"`{bar}` 0 / {LevelData.xp_for(user['level'])} XP"
                ),
                color=discord.Color.purple()
            )
            channel = self.bot.get_channel(self.config["LevelChannelID"])
            if channel:
                await channel.send(embed=embed)

        LevelData.set(message.author.id, user)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LevelSystem(bot))