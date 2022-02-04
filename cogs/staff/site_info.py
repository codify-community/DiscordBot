import discord
from discord.ext import commands
import asyncio
import datetime
from utils.mongoconnect import mongoConnect

cluster = mongoConnect()
db = cluster['discord']
conta = db['conta']
site = db['site']

class SiteInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def criar_conta(self, mem_id):
        if mem_id != 851618408965079070:
            try:    
                await conta.insert_one({"_id":mem_id, "saldo":0, "stars":[], "wallet":{}, "warnings":[], 'xp':0, "level":0, "descricao":"Use .descricao para alterar a sua descrição"})
            except:
                pass

    @commands.command(pass_context = True)
    async def edit(self, ctx, tipo : str = None, *, info : str = None):
        id = ctx.author.id
        maxs = {'ocupacao': 32, 'bio':128, 'github':128, 'habilidades':6}
        if tipo == None:
            await ctx.send('Use .edit <tipo> <info>\nUse .edit help para verificar os tipos de edição')
            return
        if tipo == 'help':
            await ctx.send('Tipos de edição:\n\n.edit ocupacao <info> (max: 32 chars)\n.edit bio <info> (max: 128 chars)\n.edit github <info> (link do teu github)\n.edit habilidades <info,info2,info3...> (max: 6 habilidades)\n\nCaso as informações fornecidas sejam maiores que o limite máximo, todo o conteudo posterior ao mesmo será ignorado.')
            return
        if info == None and tipo != 'help':
            await ctx.send('Use .edit <tipo> <info>\nUse .edit help para verificar os tipos de edição')
            return

        try:
            role_types = {"⎯⎯⎯⎯⎯⎯⠀〔Admin's〕⎯⎯⎯⎯⎯⎯⎯⠀":"staffs", "⎯⎯⎯⎯⎯⎯⎯⎯⠀〔Mod〕⎯⎯⎯⎯⎯⎯⎯⎯⎯⠀":"staffs", "⎯⎯⎯⎯⎯⎯⠀〔Dono〕⎯⎯⎯⎯⎯⎯⎯⠀":"staffs", "BOOSTER ❤️":"boosters"}

            role = role_types[ctx.author.top_role.name]

            obj = site.find_one({'_id':0})[role]

            if len(info) >= maxs[tipo] and tipo != 'habilidades':
                info = info[0:maxs[tipo]]

            if tipo == 'habilidades':
                info = info.split(',')
                if len(info) > maxs[tipo]:
                    info = info[0:maxs[tipo] - 1 ]

            for i in obj:
                if i['id'] == id:
                    i[tipo] = info
                    break

            site.update_one({'_id':0}, {'$set':{role:obj}})

            await ctx.send('Editado com sucesso!')
        except:
            await ctx.send('Erro ao editar!\n Verifique se o tipo de edição está correto.')
    


def setup(bot):
    bot.add_cog(SiteInfo(bot))