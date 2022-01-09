import logging
from datetime import datetime, timedelta
from typing_extensions import Required

from discord import Client
from discord import Cog as Extension
from discord import Member
from discord.commands import Option
from discord.commands import slash_command
from discord.commands.context import ApplicationContext
from discord.embeds import Embed

from src.accounts.users import DataBaseUser
from src.config import Config
from random import randint
import asyncio


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
        embed.description = f"{'Você' if acc == it.author else usr} tem `R$ {reais:.2f}`"
        embed.set_footer(text="Servidor Codify Community",
                         icon_url="https://cdn.discordapp.com/avatars/851618408965079070/dcaa7982cda5fc926064df5edb923aef.png?size=2048")
        await it.send_response(embed=embed)

    @slash_command(guild_ids=[743482187365613641], description="Nesse comando, você pode transferir seus reais")
    async def transferir(self, it: ApplicationContext,
                         membro: Option(Member, "Membro para transferir"), quantidade: Option(float, "quantidade")):
        self.logger.info(f"{it.author.id} tentou transferir {quantidade} reais para {membro.id}")
        if quantidade < 0:
            return await it.respond("Você não pode transferir valores negativos!")
        account = DataBaseUser(it.author.id)
        status = await account.transfer_reais(membro.id, quantidade)
        if status != True:
            await it.send_response(content=status, ephemeral=True)
        else:

            embed = Embed(color=0x738ADB, description=f"Você transferiu `R$ {quantidade}` para {membro}")
            embed.set_footer(text="Servidor Codify Community",
                             icon_url="https://cdn.discordapp.com/avatars/851618408965079070/dcaa7982cda5fc926064df5edb923aef.png?size=2048")
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
        await it.send_response(content=f"Você recebeu `R$ {qnt}` de diaria!")
    
    @slash_command(guild_ids=[743482187365613641], description="aposte dinheiros (minimo de 100 reais pra jogar)")
    async def roleta(self, it: ApplicationContext, num: Option(int, description="o numero para apostar", Required=True)):
        db_user = DataBaseUser(it.author.id)
        if await db_user.get_reais_count() < 100:
            # TODO: mudar essa mensagem
            embed = Embed(color=0x738ADB, description=f"❌ · Você não tem dinheiro suficiente")
            return await it.send_response(embed=embed)
        correct_number = randint(0, 120)
        await db_user._inc_user_coins(-100)
        embed = Embed(color=0x738ADB, description=f"Girando a roleta!!")
        embed.set_image(url="https://thumbs.gfycat.com/YellowishNewEasternglasslizard-size_restricted.gif")
        await it.send_response(embed=embed)
        await asyncio.sleep(3)
        if num == correct_number:
            await db_user._inc_user_coins(10000)
            # TODO: mudar a imagem
            embed.set_image(url="https://i.redd.it/k3dzo703mur71.png")
            embed.description = "Parabens! você ganhou 10K"
        else:
            await db_user._inc_user_coins(10000)
            # TODO: mudar a imagem
            embed.set_image(url="https://i.pinimg.com/originals/42/1e/2d/421e2de455f0918a369f67daada3590d.jpg")
            embed.description = f"Você errou! o numero era: {correct_number}"
        await it.edit(embed=embed)
        

def setup(bot: Client):
    bot.add_cog(EconomiaGeral(bot))
