import discord
from discord.ext import commands
import requests as req
import os
import asyncio
from random import randint
import re
from discord.ext import tasks
from utils.mongoconnect import mongoConnect
from utils.get_json import get_json

config = get_json("config.json")

cluster = mongoConnect()
db = cluster['discord']
conta = db['conta']

premio = []

level_num = [5,10,15,20,25,30,40,50,75,100,200,300,400,500,1000]

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def criar_conta(self, mem_id):
        if mem_id != 851618408965079070:
            try:    
                conta.insert_one({"_id":mem_id, "saldo":0, "stars":[], "wallet":{}, "warnings":[], 'xp':0, "level":0, "descricao":"Use .descricao para alterar a sua descrição"})
            except:
                pass

    @commands.Cog.listener()
    async def on_message(self, message):
        id = message.author.id

        await self.criar_conta(id)

        if message.content == f"<@!{self.bot.user.id}>":
            embed = discord.Embed(description=f'''**```Olá programador, vejo que está perdido.\n\nO prefixo do bot é "{os.getenv('prefix')}"```**''', color=0x524D68)
            embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/Qzqyb8PnlbJO12NC2At6KTKOXrrI5JIiWb1UyBmfSD8/https/cdn.discordapp.com/icons/743482187365613641/a_cdb6f45de29742c3d687597f1636f2b5.gif")
            await message.channel.send(embed=embed)

        if not message.author.bot:
            if not id in premio:
                premio.append(id)

            lvl = 0
            stats = conta.find_one({'_id':id})
            xp = stats['xp']

            while True:
                if xp < ((50*(lvl**2))+(50*lvl)):
                    break
                lvl += 1

            xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))

            nivel = 0

            if xp in range(0,25) and lvl > 1:
                next_level = int(200*((1/2)*lvl))
                nivel = int((next_level / 100)-1)

            if nivel in level_num:
                bonus = 50 * nivel
                conta.update_one({'_id':id}, {'$inc':{'saldo':bonus}})
                cmds = self.bot.get_channel(config["guild"]["channels"]["level_up"])
                await cmds.send(f'⭐ | Parabéns {message.author.mention}, você upou para o **Level {nivel}**!')
                conta.update_one({'_id':id}, {'$inc':{'xp':26}})

    @tasks.loop(minutes=1)
    async def add_xp():
        premio_temp = tuple(premio)

        if len(premio) >= 1:
            r_xp = randint(15, 25)
            premio.clear()
            conta.update_many({'_id':{'$in':premio_temp}}, {'$inc': {'xp': r_xp}})

    add_xp.start()

def setup(bot):
    bot.add_cog(Eventos(bot))