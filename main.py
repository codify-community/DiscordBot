import dotenv
import logging
import discord
from src.config import Config
from src.cogs import load_cogs
dotenv.load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
bot = discord.Bot(intents=discord.Intents.all())
config = Config()
if config.isOnDevEnv:
    logging.warning("Bot is running on development environment")
load_cogs(bot)
bot.run(config.token)
