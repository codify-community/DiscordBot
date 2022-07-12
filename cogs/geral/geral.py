import discord
from discord.ext import commands
from loaders.get_json import get_json

commands_ = get_json("commands.json")

class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #===================================================
    #                      GERAL                       =
    #===================================================

    @commands.command(aliases=['h', 'ajuda', 'comandos', 'commands'])
    async def help(self, ctx, comando : str = None):
        if comando == None:
            embed = discord.Embed(description = ':book: **Ajuda**', color = 0xFECD00)
            embed.add_field(name = ':gear: Geral', value = f'''`embed` | Envia uma mensagem em formato embed
    `ping` | Mostra a latência atual do bot
    `help` | Mostra está mensagem''', inline = False)
            embed.add_field(name = ':coin: Cripto', value = f'''`exchange` | Dados gerais sobre as criptomoedas principais
    `comprar` | Comprar criptomoedas
    `vender` | Vender criptomoedas
    `wallet` | Checar sua carteira ou de outros usuários''', inline = False)
            embed.add_field(name = ':money_with_wings: Economia', value = f'''`saldo` | Checar seu saldo ou de outro usuário em dinheiro
    `transferir` | Pagar\\transferir para outro usuário
    `descricao` | Modificar texto da descrição do perfil
    `rank` | Ranking de usuários
    `diario` | Resgatar prêmio diário
    `roleta` | Apostar dinheiro na roleta da sorte
    `apostar` | Apostar em outros usuários''', inline = False)
            embed.add_field(name = ':star2: Estrelas', value = f'''`stars` | Checar quantidade de estrelas dada ao ajudante
    `avaliar` | Avaliar ajudante
    `desavaliar` | Retira avaliação dada ao ajudante''', inline = False)
            embed.add_field(name = ':tools: Moderação', value = f'''`mute` | Mutar membro
    `kick` | Expulsar membro do servidor
    `ban` | Banir membro do servidor
    `warn` | Avisar membro
    `warnings` | Checa os avisos ativos do membro
    `unwarn` | Retira aviso do membro
    `limpar` | Apaga as mensagens mais recentes do bate-papo atual
    `lock` | Trava e Destrava um canal
    `changelog | Cria um change log`''', inline = False)
            embed.set_footer(text = 'Utilize .help <comando> para mais informações')
        elif comando.lower() in commands_:
            embed = discord.Embed(title=f'Informações complementares do comando {commands_[comando.lower()]["name"]}', color = 0xFECD00)
            embed.add_field(name = '🖖 convenções', value=''' `<>` | Parâmetro Obrigatório
`[]` | Parâmetro Opcional''', inline = False)
            embed.add_field(name="Exemplo", value=commands_[comando.lower()]["value"], inline = False)
        else:
            embed = discord.Embed(description = ':book: **Ajuda**', color = 0xFECD00)
            embed.add_field(name = ':x: Comando não encontrado', value = f'`O comando {comando}` não foi encontrado', inline = False)

        await ctx.channel.send(embed = embed)

    @commands.command(pass_context=True)
    async def embed(self, ctx, *, arg):
        await ctx.message.delete()

        em = discord.Embed(description=arg, color=0xFECD00)
        await ctx.channel.send(embed=em)

    @commands.command(pass_context = True, aliases = ['latencia'])
    async def ping(self, ctx):
        embed = discord.Embed(title = 'Latência', description = f'A latência atual é de **{round(self.bot.latency * 1000)}ms**', color = 0xffff00)
        embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2012/04/01/19/21/exclamation-mark-24144_960_720.png')
        await ctx.channel.send(embed = embed)

def setup(bot):
    bot.add_cog(Geral(bot))
