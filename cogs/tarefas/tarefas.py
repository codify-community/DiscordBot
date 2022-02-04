import discord
from discord.ext import commands, tasks
import asyncio
import datetime
from utils.mongoconnect import mongoConnect
import requests as req
import json
import pprint

import os

path = os.getcwd()

with open(f"{path}/config.json") as json_file:
    config = json.load(json_file)

cluster = mongoConnect()
db = cluster['discord']
site = db['site']
logs = db['logs']

async def find_users():
    info = site.find_one({'_id': 0})
    staffs = info['staffs']
    boosters = info['boosters']
    return staffs, boosters

def get_updated_users(discord_users, db_users):
    updated_users = []

    for user in discord_users:

        db_user = {}
        
        for i in db_users:
            if user["id"] == i["id"]:
                db_user = i
                break
        
        if db_user:
            db_user.update(user)
            updated_users.append(db_user)
        else:
            user.update({
                'habilidade': ["Nenhuma"],
                'bio': "Biografia Não Definida",
                'ocupacao': "",
                'github': 'https://github.com/codify-community'
            })
            
            updated_users.append(user)
            
    return updated_users
    

class Tarefas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @tasks.loop(minutes=5)
        async def send_status():
            hr = datetime.datetime.now()
            logs.find_one_and_update({'_id': 0}, {'$set': {'last_ping': hr}})
        send_status.start()

        @tasks.loop(hours=24)
        async def keep_api_alive():
            req.get('https://codify-site-api.herokuapp.com/api/home')

        @tasks.loop(minutes=10)
        async def get_info(self):
            guild = self.bot.get_guild(743482187365613641)
            #member quant
            member_count = int(guild.member_count)
            #channels quant
            channel_count = len(guild.channels)
            #staff quant
            staff_count = 0

            '''
                * Pegar os staffs e boosters do banco de dados;
                * Pegar os staffs e boosters atuais do discord;
                * Comparar arrays:
                    - Se o usuário existe no banco de dados:
                        - Verificar se existe alguma propriedade diferente;
                    - Se não:
                        - Adicionar o usuário a lista de usuários;
                    
                * Verificar se algum usuário existe no banco de dados, mas não existe mais no array 
                do usuários do discord
            '''

            db_staffs, db_boosters = [], []
            discord_staffs, discord_boosters = [], []

            for member in guild.members:
                if member.bot: continue
                    
                for role in member.roles:
                    if role.id in config['guild']['roles']['staffs']:
                        
                        user = await self.bot.fetch_user(member.id)

                        staff = {
                            'id': user.id,
                            'role': config['guild']['roles_name'][str(role.id)],
                            'name': user.name,
                            'pfp': str(user.avatar_url)
                        }

                        discord_staffs.append(staff)
                        break

                    elif role.id in config['guild']['roles']['boosters']:

                        user = await self.bot.fetch_user(member.id)

                        booster = {
                            'id': user.id,
                            'role': config['guild']['roles_name'][str(role.id)],
                            'name': user.name,
                            'pfp': str(user.avatar_url)
                        }
                        
                        discord_boosters.append(booster)
                        break
            
            updated_staffs = get_updated_users(discord_staffs, db_staffs)
            updated_boosters = get_updated_users(discord_boosters, db_staffs)
            
            site.find_one_and_update({'_id': 0}, {'$set': {'staffs': updated_staffs, 'boosters': updated_boosters}})

        get_info.start(self)

def setup(bot):
    bot.add_cog(Tarefas(bot))
