from discord import Cog as Extension
from discord import Client
from discord.embeds import Embed
from discord.ext.commands.cooldowns import BucketType
from src.config import Config
from src.accounts.users import DataBaseUser
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.commands import slash_command
from datetime import datetime, timedelta
from discord import Member
import logging
class EconomiaGeral(Extension):
    def __init__(self, bot: Client):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        self.config = Config()
    @slash_command(guild_ids=[743482187365613641], description="Nesse comando, você vê quanto reais você tem")
    async def saldo(self, it: ApplicationContext, user: Option(Member, "Membro", required=False)):
        acc = user or it.author
        account = DataBaseUser(acc.id)
        reais = await account.get_reais_count()
        usr = acc.nick or acc.name
        embed = Embed(title=f"Saldo de {usr}" if acc !=
                      it.author else "Seu Saldo", color=0x738ADB)
        embed.description = f"{'Você' if acc == it.author else usr } tem `R${reais}`"
        await it.send_response(embed=embed)
    @slash_command(guild_ids=[743482187365613641], description="Nesse comando, você pode transferir seus reais")
    async def tranferir(self, it: ApplicationContext,
         membro: Option(Member, "Membro para transferir"), quantidade: Option(int, "quantidade")):
        self.logger.info(f"{it.author.id} tentou transferir {quantidade} reais para {membro.id}")
        if quantidade < 1:
            return await it.respond("Você não pode transferir menos de 1 reais!")
        account = DataBaseUser(it.author.id)
        status = await account.transfer_reais(membro.id, quantidade)
        if status != True:
            await it.send_response(content=status, ephemeral=True)
        else:
            embed = Embed(color=0x738ADB, description=f"Você transferiu `R${quantidade}` para {membro.name}")
            await it.send_response(embed=embed)
    @slash_command(guild_ids=[743482187365613641], description="Nesse comando, você pode pegar sua diaria")
    async def diaria(self, it: ApplicationContext):
        if it.author.id in self.cache:
            cache: datetime = self.cache[it.author.id]
            cache2 = cache
            cache2 += timedelta(days=1)
            if cache != cache2:
                return await it.respond("Você já pegou sua diaria hoje!", ephemeral=True)
        else:
            self.cache[it.author.id] = datetime.today()
        user = DataBaseUser(it.author.id)
        qnt = await user.daily()
        await it.send_response(content=f"Você recebeu `R${qnt}` de diaria!")
    

def setup(bot: Client):
    bot.add_cog(EconomiaGeral(bot))