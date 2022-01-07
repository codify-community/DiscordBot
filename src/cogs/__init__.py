import os
import logging
def load_cogs(bot):
    """
    Loads all cogs in the cogs folder.
    """
    logger = logging.getLogger(__name__)
    cog_paths = ["events", "geral", "crypto"]
    for path in cog_paths:
        for filename in os.listdir(f"./src/cogs/{path}"):
            if filename.endswith(".py") and filename != "__init__.py":
                logger.info(f"[COG LOADER] Loading {path}/{filename}")
                bot.load_extension(f"src.cogs.{path}.{filename[:-3]}")
    logger.info("[COG LOADER] All cogs loaded!")