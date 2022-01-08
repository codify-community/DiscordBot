import datetime
import logging
from asyncio import sleep

from discord import Client
from discord import Cog as Extension
from discord import Game
from discord.ext import tasks

from src.config import Config
from src.database import connect_database
from src.utils import proc


class Events(Extension):
    def __init__(self, bot: Client):
        self.bot = bot
        self.config = Config()
        self.logger = logging.getLogger(__name__)

    @Extension.listener()
    async def on_ready(self):
        await connect_database()

        self.logger.info("Received Ready Event.")

        @tasks.loop(seconds=15)
        async def update_status():
            status = lambda text: self.bot.change_presence(
                activity=Game(name=text, timestamps={"start": datetime.datetime.now().ctime()}))
            await status(f"Versão atual: {self.config.version}")
            await sleep(15)
            if self.config.isOnDevEnv:
                await status(f"Aviso! Estou em um ambiente de desenvolvimento.")
                await sleep(15)
                await status(f"Usando {proc.get_current_memory_usage_by_python()} MB de Ram!")
                await sleep(15)
            await status("Sim, eu sou um bot.")
            await sleep(15)
            await status("Estou ajudando a codify!")
            await sleep(15)
            await status("Re-Escrito pelo yxqsnz!")
            await sleep(15)
            await status("Acesse: codifycommunity.tk")

        await self.bot.get_channel(self.config.logsChannel).send("Bot iniciado com sucesso!\n")
        update_status.start()


def setup(bot):
    bot.add_cog(Events(bot))
