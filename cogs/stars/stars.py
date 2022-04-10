import discord
from discord.ext import commands
import requests as req
import os
from dotenv import load_dotenv
import asyncio
from random import randint
import re
from discord.ext import tasks
from util.mongoconnect import mongoConnect
import datetime

load_dotenv()
env = os.getenv('env')

cluster = mongoConnect()
db = cluster['discord']
conta = db['conta']

premio = []

class Stars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def criar_conta(self, mem_id):
        if mem_id != 851618408965079070:
            try:    
                conta.insert_one({"_id":mem_id, "saldo":0, "stars":[], "wallet":{}, "warnings":[], 'xp':0, "level":0, "descricao":"Use .descricao para alterar a sua descrição"})
            except:
                pass


    @commands.command()
    async def stars(self, ctx, member : discord.Member = None):
        id = ctx.author.id
        mention = ctx.author.mention
        name = ctx.author.name
        if member != None:
            id = member.id
            mention = member.mention
            name = member.name
        await self.criar_conta(id)
        stats = conta.find_one({'_id':id})['stars']
        if len(stats) == 0:
            await ctx.send(embed = discord.Embed(description=f'{member.mention} ainda não possui Stars.', color=0x1CFEFE))
            return
        await ctx.send(embed = discord.Embed(title = f'STARS DE {name}', description=f"{mention} possui {len(stats)} Stars!\n Acesso nosso site para conferir todas as pessoas que foram ajudadas por este usuário (em breve...)", color=0x1CFEFE))

    @commands.command()
    async def avaliar(self, ctx, member : discord.Member = None, desc : str = None):
        id = ctx.author.id
        await self.criar_conta(id)
        await self.criar_conta(member.id)
        if member == None or member.id == id:
            await ctx.send(embed = discord.Embed(description='você precisa marcar um membro **válido** para dar uma Star', color=0xE63E43))
            return
        if desc == None:
            await ctx.send(embed = discord.Embed(description='Você precisa definir uma descrição!', color=0xE63E43))
            return
        data = datetime.datetime.now()
        if env == 'prod':
            data = data - datetime.timedelta(hours=3)
        
        already = False
        stats = conta.find_one({'_id':member.id})['stars']
        print(stats)
        for i in stats:
            print(id)
            if i['id'] == id:
                already = True
                print('already')
                break
        if already:
            await ctx.send(embed = discord.Embed(description='Você já deu uma Star para esse membro', color=0xE63E43))
            return
        conta.find_one_and_update({'_id':member.id}, {'$push':{'stars':{'id':id, 'quant': 1, 'desc':desc, 'data':data}}})
        await ctx.send(embed = discord.Embed(description='Star enviada com sucesso!', color=0x1CFEFE))



    @commands.command()
    async def desavaliar(self, ctx, member : discord.Member = None, desc : str = None):
        id = ctx.author.id
        await self.criar_conta(id)
        if member == None or member.id == id:
            await ctx.send(embed = discord.Embed(description='você precisa marcar um membro para remover a Star', color=0xE63E43))
            return
        if desc == None:
            await ctx.send(embed = discord.Embed(description='Você precisa definir uma descrição para filtrar!', color=0xE63E43))
            return
        try:
            conta.find_one_and_update({'_id':member.id}, {'$pull':{'stars':{'desc':desc}}})
            await ctx.send(embed = discord.Embed(description='Star removida com sucesso!', color=0x1CFEFE))
        except:
            await ctx.send(embed = discord.Embed(description='Star não encontrada!', color=0xE63E43))



def setup(bot):
    bot.add_cog(Stars(bot))