from discord import Cog as Extension
from discord.commands import slash_command
from discord.commands.context import ApplicationContext
from src.utils import proc
from src.config import Config
from discord import Client
import logging

from discord.embeds import Embed
class GeralExtension(Extension):
    def __init__(self, bot: Client):
        self.bot = bot
        self.config = Config()
        self.logger = logging.getLogger(__name__)
    @slash_command(guild_ids=[743482187365613641], description="Nesse comando você pode ver minhas informações!")
    async def status(self, it: ApplicationContext):
        embed = Embed()
        embed.color = 0x738ADB
        embed.title = "Minhas informações"
        embed.description = f""":call_me: **·** Olá! Eu sou o Codify, feito pelo [**Yxqsnz**](https://discord.com/users/615176567567548446), [**Jv**](https://discord.com/users/693639831443734538) e [**Aeon**](https://discord.com/users/470045008633004044).
         Isso também inclue os contribuidores da Codify Community.
 
        :desktop: **·** Uso de Ram: [{proc.get_current_memory_usage_by_python()}M](https://codifycommunity.tk)
        :satellite: **·** Latência: [{self.bot.latency * 1000:.2f}ms](https://codifycommunity.tk)
        :robot: **·** Versão atual: [{self.config.version}](https://codifycommunity.tk)
        """
        embed.set_footer(text="Servidor Codify Community", icon_url="https://cdn.discordapp.com/avatars/851618408965079070/dcaa7982cda5fc926064df5edb923aef.png?size=2048")
        await it.respond(embed=embed)
def setup(bot):
    bot.add_cog(GeralExtension(bot))