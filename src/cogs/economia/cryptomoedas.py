import logging
import random
from datetime import datetime

# async supremacy
import aiohttp
from discord import Client
from discord import Cog as Extension
from discord import Member
from discord.commands import Option
from discord.commands import slash_command
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import tasks

from src.accounts.users import DataBaseUser
from src.config import Config


class CryptoCached:
    def __init__(self, lastPrice: float, priceChangePercent: float, name: str):
        self.lastPrice = lastPrice
        self.priceChangePercent = priceChangePercent
        self.name = name

    def fmtPriceChangePercent(self):
        s = str(self.priceChangePercent)
        if not s.startswith("-"):
            return f"+{s}%"
        else:
            return f"{s}%"


cryptos = {'BTC': 'BTCBRL', 'ETH': 'ETHBRL', 'BNB': 'BNBBRL', 'LTC': 'LTCBRL',
           'AXS': 'AXSBRL', 'SOL': 'SOLBRL', 'DOT': 'DOTBRL', 'LINK': 'LINKBRL', 'FTM': 'FTMBRL'}
cryptos_inverso = {'BTCBRL': 'BTC', 'ETHBRL': 'ETH', 'BNBBRL': 'BNB', 'LTCBRL': 'LTC',
                   'AXSBRL': 'AXS', 'SOLBRL': 'SOL', 'DOTBRL': 'DOT', 'LINKBRL': 'LINK', 'FTMBRL': 'FTM'}
cryptos_nome = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance Coin', 'LTC': 'Litecoin',
                'AXS': 'Axie Infinity', 'SOL': 'Solano', 'DOT': 'Polkadot', 'LINK': 'Chainlink', 'FTM': 'Fantom'}


class CryptoExtension(Extension):
    def __init__(self, bot: Client):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.config = Config()
        self.last_update = datetime.now()

        @tasks.loop(minutes=15)
        async def update_cache():
            await self.bot.get_channel(self.config.logsChannel).send("Atualizando cache...")
            async with aiohttp.ClientSession() as session:
                self.cache = {}
                for crypto in cryptos_inverso.keys():
                    try:
                        async with session.get(f'https://api.binance.com/api/v3/ticker/24hr?symbol={crypto}') as resp:
                            data = await resp.json()
                            self.cache[cryptos_inverso[crypto]] = CryptoCached(float(data['lastPrice']), float(
                                data['priceChangePercent']), cryptos_nome[cryptos_inverso[crypto]])
                    except Exception as e:
                        self.logger.error(f'Erro ao atualizar cache: {e}')
                        await self.bot.get_channel(self.config.logsChannel).send(f"Erro ao atualizar cache: {e}")

            await self.bot.get_channel(self.config.logsChannel).send("Cache atualizado com sucesso!")
            self.last_update = datetime.now()

        self.upd_cache = update_cache

    @slash_command(guild_ids=[743482187365613641],
                   description="Nesse comando, você pode consultar o preço de um dos principais crypto-coins do mercado")
    async def exchange(self, it: ApplicationContext):
        embed = Embed(title="Preço de criptomoedas", color=0x738ADB)
        emotes = ['<:binancecoin:926324388725424138>', '<:ethereum:926324233523560478>',
                  '<:binancecoin:926324388725424138>', '<:litecoin:926324504156852224>',
                  '<:axye:926324690916618260>', '<:solano:926324887407194132>', '<:polkadot:926324993569226782>',
                  '<:chainlink:926325188969246730>', '<:pancakeswap:926325842236305468>']
        graphs = 'https://coinmarketcap.com/pt-br/currencies/bitcoin/ https://coinmarketcap.com/pt-br/currencies/ethereum/ https://coinmarketcap.com/pt-br/currencies/binance-coin/ https://coinmarketcap.com/pt-br/currencies/litecoin/ https://coinmarketcap.com/pt-br/currencies/axie-infinity/ https://coinmarketcap.com/pt-br/currencies/solana/ https://coinmarketcap.com/pt-br/currencies/polkadot-new/ https://coinmarketcap.com/pt-br/currencies/chainlink/ https://coinmarketcap.com/pt-br/currencies/fantom/'.split()
        dicas = [
            "Compre Criptos quando estiverem em baixa para vende-las quando estiverem em alta! Mas Cuidado! Nem sempre é assim.",
            "Você pode ver os gráficos dos preços de criptomoedas clicando no preço da criptomoeda."]
        tip = random.choice(dicas)
        for (emote, graph, val) in zip(emotes, graphs, self.cache.keys()):
            crypto = self.cache[val]
            embed.add_field(name=f"{emote} {crypto.name}({val})",
                            value=f"[R$ {crypto.lastPrice:.2f} ({crypto.fmtPriceChangePercent()})]({graph})",
                            inline=True)
        embed.description = f"""
💡· Dica: {tip}
🗒️· Pro Tip: Você pode vender suas cryptos usando /vender e comprar com /comprar
        """
        embed.timestamp = self.last_update
        embed.set_footer(text="Servidor Codify Community",
                         icon_url="https://cdn.discordapp.com/avatars/851618408965079070/dcaa7982cda5fc926064df5edb923aef.png?size=2048")
        await it.respond(embed=embed)

    @slash_command(guild_ids=[743482187365613641], description="Nesse comando, você pode vender suas cryptomoedas")
    async def vender(self, it: ApplicationContext,
                     moeda: Option(str, "A Moeda que você quer comprar", default="BTC", choices=cryptos),
                     quantidade: Option(int, "Quantidade de moedas que você quer comprar", default=1)):

        if quantidade < 1:
            return await it.respond("Você não pode vender menos de 1 moeda!", ephemeral=True)
        user = DataBaseUser(it.author.id)
        status = await user.sell_coins(
            moeda, self.cache[moeda].lastPrice, quantidade)
        if status != True:
            await it.send_response(status, ephemeral=True)
        else:
            embed = Embed(color=0x738ADB,
                          description=f"Você vendeu {quantidade} {moeda} por `R${self.cache[moeda].lastPrice * quantidade:.2f}`")
            await it.send_response(embed=embed)

    @slash_command(guild_ids=[743482187365613641], description="Nesse comando, você pode comprar suas cryptomoedas")
    async def comprar(self, it: ApplicationContext,
                      moeda: Option(str, "A Moeda que você quer comprar", default="BTC", choices=cryptos),
                      quantidade: Option(int, "Quantidade de moedas que você quer comprar", default=1)):

        if quantidade < 1:
            return await it.respond("Você não pode comprar menos de 1 moeda!")
        account = DataBaseUser(it.author.id)
        status = await account.buy_coin(moeda, self.cache[moeda].lastPrice, quantidade)
        if status != True:
            await it.send_response(content=status, ephemeral=True)
        else:
            embed = Embed(color=0x738ADB,
                          description=f"Você comprou {quantidade} {moeda}(s) por `R${self.cache[moeda].lastPrice * quantidade:.2f}`")

            await it.send_response(embed=embed)

    @slash_command(guild_ids=[743482187365613641], description="Nesse comando, você vê quanto reis você tem")
    async def carteira(self, it: ApplicationContext, user: Option(Member, "Membro", required=False)):
        acc = user or it.author
        account = DataBaseUser(acc.id)
        usr = acc.nick or acc.name
        embed = Embed(title=f"Carteira de {usr}" if acc !=
                                                    it.author else "Sua Carteira", color=0x738ADB)
        wallet = await account.get_wallet()
        coins_str = '\n'.join(
            [f'> {key} - `{wallet[key]}` moeda(s)' for key in wallet.keys()])
        estimativa = sum([wallet[key] * self.cache[key].lastPrice for key in wallet.keys()])
        if wallet == {}:
            embed.description = f"{'Você' if acc == it.author else usr}  não tem nenhuma moeda em sua carteira"
        else:
            embed.description = f"""{'Você' if acc == it.author else usr} tem:
            {coins_str}
            Estimativa: `R$ {estimativa:.2f}`
            """
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/760531609261834250/929335772715315240/emoji.png')
        embed.set_footer(text="Servidor Codify Community",
                         icon_url="https://cdn.discordapp.com/avatars/851618408965079070/dcaa7982cda5fc926064df5edb923aef.png?size=2048")
        await it.respond(embed=embed)

    @Extension.listener()
    async def on_ready(self):
        self.upd_cache.start()


def setup(bot):
    bot.add_cog(CryptoExtension(bot))
