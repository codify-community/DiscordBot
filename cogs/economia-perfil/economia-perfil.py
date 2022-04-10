import discord
from discord.ext import commands
import requests as req
from random import randint
import asyncio
from discord.ext.commands.core import cooldown
from util.mongoconnect import mongoConnect

cluster = mongoConnect()
db = cluster['discord']
conta = db['conta']
server = db['server']
membros = db['membros']

talk_channels = []
premio = []
custo_up_2 = 20000

class Economiaperfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def formatar_tempo(self, seconds):
        total_segs = int(seconds)
        horas = total_segs // 3600
        dias = horas//86400
        segs_restantes = total_segs % 3600
        minutos = segs_restantes // 60
        segs_restantes_final = segs_restantes % 60
        if (horas >= 24): 
            dias = int(horas / 24)
            horas = int(horas % 24)
        
        if dias != 0:
            return f'{dias} dia(s)'
        elif horas != 0:
            return f'{horas} hora(s)'
        elif minutos != 0:
            return f'{minutos} minuto(s)'
        elif segs_restantes_final != 0:
            return f'{segs_restantes_final} segundo(s)'

    async def criar_conta(self, mem_id):
        if mem_id != 851618408965079070:
            try:    
                await conta.insert_one({"_id":mem_id, "saldo":0, "stars":[], "wallet":{}, "warnings":[], 'xp':0, "level":0, "descricao":"Use .descricao para alterar a sua descrição"})
            except:
                pass
    #===================================================
    #                     XP E PERFIL                  =
    #===================================================
    @commands.command(pass_context=True, aliases=['atm', 'bal', 'balance'])
    async def saldo(self, ctx, member : discord.Member = None):
        await self.criar_conta(ctx.author.id)
        if member == None:
            id = ctx.author.id
            member = ctx.author
        else:
            await self.criar_conta(member.id)
            id = int(member.id)
        await ctx.channel.send(embed = discord.Embed(title = f'SALDO DE {member.name.upper()}:', description = f'💸 {conta.find_one({"_id":id})["saldo"]} Reais', color=0x1CFEFE))

    @commands.command(pass_context=True, aliases=['pagar', 'transf'])
    async def transferir(self, ctx, member : discord.Member = None, quant : int = None):
        if member == None or quant == None:
            id = ctx.author.id
            await ctx.channel.send(embed = discord.Embed(description = f'Você precisa informar para quem quer transferir e a quantidade de dinherio. Ex: .transferir @jv 1000', color=0x1CFEFE))
        else:
            if not '-' in str(quant) and quant != 0:
                if member.id != ctx.author.id:
                    id = ctx.author.id
                    await self.criar_conta(id)
                    other_id = member.id
                    await self.criar_conta(other_id)
                    if conta.find_one({'_id':id})['saldo'] >= quant:
                        conta.find_one_and_update({'_id':id}, {'$inc':{'saldo':-quant}})
                        conta.find_one_and_update({'_id':other_id}, {'$inc':{'saldo':quant}})
                        transacoes = self.bot.get_channel(743492526542946424)
                        emb = discord.Embed(title = f'{ctx.author.name.upper()} FEZ UMA TRANSFERENCIA PARA {member.name.upper()}:', description = f'{ctx.author.mention} transferiu {quant} reais para {member.mention}', color=0x1CFEFE)
                        await ctx.channel.send(embed = emb)
                        await transacoes.send(embed = emb)
                    else:
                        await ctx.channel.send(embed = discord.Embed(description = f'Você não tem saldo suficiente para concluir está transação', color=0x1CFEFE))
                else:
                    await ctx.channel.send('**Porquê você quer transferir um valor para você mesmo?\nInforme um membro válido da próxima vez!**')
            else:
                await ctx.channel.send('**Como você vai trasnferir um valor negativo ou nulo?\nInforme um valor correto da próxima vez!**')


    @commands.command(pass_context=True, aliases=['desc', 'description'])
    async def descricao(self, ctx, *, arg = None):
        id = ctx.author.id
        await self.criar_conta(id)
        if arg == None:
            await ctx.channel.send(embed = discord.Embed(description = f'Você precisa informar qual será a sua nova descrição. Ex: .descricao minha nova descrição é essa!', color = 0xff0000))
        else:
            if len(arg) >= 65:
                arg = list(arg)
                lista = arg[0:57]
                arg = ''
                for i in lista:
                    arg += i
                arg += '...'
            conta.find_one_and_update({'_id':id}, {'$set':{'descricao':arg}})
            await ctx.channel.send(embed = discord.Embed(title='SUA DESCRIÇÃO FOI ALTERADA', description = f'{ctx.author.name}, sua descrição foi alterada para: "{arg}"', color = 0xffffff))
            

    @commands.command(aliases=['ranking', 'perfil', 'profile', 'exp', 'experience', 'level', 'xp'])
    async def rank(self, ctx, membro : discord.Member=None):
        if membro == None:
            user = ctx.author
        else:
            user = membro
    
        stats = conta.find_one({'_id':user.id})
        await self.criar_conta(user.id)
        xp = stats['xp']
        lvl = 0
        rank = 0    
        while True:
                if xp < ((50*(lvl**2))+(50*lvl)):
                    break
                lvl += 1
        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
        boxes = int((xp/(200*((1/2) * lvl)))*20)
        rankings = conta.find().sort('xp',-1)
        for x in rankings:
            rank += 1
            if stats['_id'] == x['_id']:
                break 
        next_level = int(200*((1/2)*lvl))
        nivel = int((next_level / 100)-1)
        porcent = int ((xp/next_level)*100)
        saldo = conta.find_one({'_id':user.id})['saldo']
        embed = discord.Embed(title =f"PERFIL DE {user.name}:", color = 0x1CFEFE)
        embed.add_field(name = '📝 Nome', value = f'{user.mention}', inline = True)
        embed.add_field(name = '📝 Descrição', value = f'{user.mention}', inline = True)
        embed.add_field(name = '<a:ff_fogo_padrao:809486155815845898> XP', value = f'` {xp} XP `', inline = True)
        embed.add_field(name = '💸 saldo', value = f'` {saldo} FP `', inline = True)
        embed.add_field(name = '⭐ Nível', value = f'`⠀⠀{nivel}⠀⠀`', inline = True)
        embed.add_field(name = '🏆 Rank', value = f'`⠀{rank}°⠀`', inline = True)
        embed.add_field(name = f'Barra de Progresso ⠀⠀⠀⠀⠀   ⠀⠀ ⠀⠀⠀{xp}/{next_level} XP ({porcent}%)', value = boxes*':blue_square:'+ (20-boxes)*':white_large_square:', inline = False)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.channel.send(embed=embed)



    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command( pass_context=True, aliases=['daily'])
    async def diario(self, ctx):
        id = ctx.message.author.id
        await self.criar_conta(id)
        
        nsort = randint(1, 30)
        conta.find_one_and_update({'_id':id}, {'$inc':{'saldo':nsort}})


        em = discord.Embed(title = f'Você recebeu {nsort} reais no seu bonus diario.', description="Volte amanhã para poder pega-lo novamente.", color=0xE63E43)
        em.set_thumbnail(url='https://images.vexels.com/media/users/3/146457/isolated/preview/2bba99c4323c66745b5584ef7a1163a2-open-red-wrap-gift-box-by-vexels.png')
        await ctx.channel.send(embed = em)    
    @diario.error
    async def diario_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'Esse comando está em cooldown. Você poderá **usar novamente em {}**'.format(Economiaperfil.formatar_tempo(self, error.retry_after))
            await ctx.send(msg)
        else:
            raise error



    @commands.command()
    async def roleta(self, ctx, arg:int):
        id = ctx.message.author.id
        await self.criar_conta(id)
        if not '-' in str(arg) and arg != 0:
            if arg >= 1 and arg <=60:
                if conta.find_one({'_id':id})['saldo'] >= 100:
                    conta.find_one_and_update({'_id':id}, {'$inc':{'saldo':-100}})
                    em = discord.Embed(title = f'Roleta da sorte', description="Você gastou 100 reais nesta aposta.\nGirando a roleta...", color=0xE63E43)
                    em.set_image(url='https://i.pinimg.com/originals/8f/5c/73/8f5c73ea3f81efb84f9043608cfb3467.gif')
                    roleta = await ctx.channel.send(embed = em)
                    await asyncio.sleep(3)
                    num_roleta = randint(1,60)
                    if arg == num_roleta:
                        conta.find_one_and_update({'_id':id}, {'$inc':{'saldo':1000}})
                        await roleta.edit(embed = discord.Embed(title = f'A roleta parou no número {num_roleta}', description = f'{ctx.author.mention} você ganhou 1000 reais na roleta!!', color=0xE63E43))
                    else:
                        await roleta.edit(embed = discord.Embed(title = f'A roleta parou no número {num_roleta}', description = f'{ctx.author.mention} não foi dessa vez...\nTente novamente, boa sorte!', color=0xE63E43))
                else:
                    await ctx.channel.send(embed = discord.Embed(title='Dinheiro insuficiente!', description = f'{ctx.author.mention} você não tem dinheiro suficiente para a aposta. O valor **mínimo é de 100 reais**', color=0xFF0000))
            else:
                await ctx.channel.send(embed = discord.Embed(description = f'{ctx.author.mention} você deve escolher um número **entre 1 e 60**', color=0xE63E43))
        else:
            await ctx.channel.send('**Como você vai aspostar um valor negativo ou nulo na roleta?\nInforme um valor correto da próxima vez!**')
    @roleta.error
    async def roleta_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = discord.Embed(description='Você deve escolher um número **entre 1 e 60**\nEx: .roleta 7', color=0xE63E43))
        else:
            raise error


    
    @commands.command(pass_context=True, aliases=['aposta', 'bet'])
    async def apostar(self, ctx, member : discord.Member = None, quant : int = None):
        if member == None:
            await ctx.channel.send(embed = discord.Embed(description = f'Você precisa informar para quem fará a aposta. Ex: .apostar @jv 1000', color = 0xff0000))
        elif quant == None:
            await ctx.channel.send(embed = discord.Embed(description = f'Você precisa informar o valor da aposta. Ex: .apostar @jv 1000', color = 0xff0000))
        else:
            if not '-' in str(quant) or quant == 0:
                if member.id != ctx.author.id:
                    id = ctx.author.id
                    other_id = member.id
                    await self.criar_conta(id)
                    await self.criar_conta(other_id)
                    aposta = await ctx.channel.send(embed=discord.Embed(title='APOSTA', description = f'{ctx.author.mention} quer fazer uma aposta de {quant} reais para {member.mention}.\nAssim que o {member.mention} clicar em "✅", a aposta será inciada.', color=0x1CFEFE))
                    await aposta.add_reaction('✅')
                    await aposta.add_reaction('🛑')
                    user_id = ctx.author.id
                    member_id = member.id
                    quant_aposta = quant
                else:
                    await ctx.channel.send(embed = discord.Embed(description = '**Por que você quer apostar um valor com você mesmo?\nInforme um membro válido da próxima vez!**', color=0xff0000))
            else:
                await ctx.channel.send(embed = discord.Embed(description = '**Como você vai apostar um valor negativo ou nulo?\nInforme um valor correto da próxima vez!**', color=0xff0000))

        def check(reaction, user):
            return (user == member or user == ctx.author) and str(reaction.emoji) in ['✅', '🛑'] and reaction.message.id == aposta.id
            #verifica a pessoa mencionada, reacções e id da mensangem reagida
        while True:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=3600, check=check)
            emoji = str(reaction.emoji)
            if emoji == "✅" and user == member:
                await aposta.clear_reactions()
                user_saldo = conta.find_one({'_id':user_id})['saldo']
                member_saldo = conta.find_one({'_id':member_id})['saldo']
                if user_saldo >= quant_aposta:
                    if member_saldo >= quant_aposta:
                        moeda = randint(0, 1)   
                        if moeda == 0:
                            await ctx.channel.send(embed = discord.Embed(description = f'<@{user_id}> ganhou a aposta de {quant_aposta} reais.',color=0x1CFEFE))
                            conta.find_one_and_update({'_id':user_id}, {'$inc':{'saldo':quant_aposta}})
                            conta.find_one_and_update({'_id':member_id}, {'$inc':{'saldo':-quant_aposta}})
                        else:
                            await ctx.channel.send(embed = discord.Embed(description = f'<@{member_id}> ganhou a aposta de {quant_aposta} reais.', color=0x1CFEFE))
                            conta.find_one_and_update({'_id':member_id}, {'$inc':{'saldo':quant_aposta}})
                            conta.find_one_and_update({'_id':user_id}, {'$inc':{'saldo':-quant_aposta}})
                    else:
                        await ctx.channel.send(embed = discord.Embed(title='Dinheiro insuficiente!', description = f'<@{member_id}> você não tem dinheiro suficiente para a aposta.', color=0xFF0000))
                else:
                    await ctx.channel.send(embed = discord.Embed(title='Dinheiro insuficiente!', description = f'<@{user_id}>, você não tem dinheiro suficiente para a aposta.', color=0xFF0000))
                break
            if emoji == '🛑' and (user == ctx.author or user == member):
                await aposta.clear_reactions()
                await aposta.edit(embed = discord.Embed(title='APOSTA CANCELADA!', description = f'A aposta de {quant_aposta} reais foi cancelada', color=0xFF0000))
                break




def setup(bot):
    bot.add_cog(Economiaperfil(bot))
