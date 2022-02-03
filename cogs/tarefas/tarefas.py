import discord
from discord.ext import commands, tasks
import asyncio
import datetime
from utils.mongoconnect import mongoConnect
import requests as req
  
cluster = mongoConnect()
db = cluster['discord']
site = db['site']
logs = db['logs']

async def find_staff():
    info = site.find_one({'_id': 0})
    staffs = info['staffs']
    boosters = info['boosters']
    return [staffs, boosters]

def get_update(member, db_user):

    discord_member = {
        name: member.name,
        pfp: str(member.avatar_url),
    }

    for user in db_staffs:
        if user['id'] == member.id:
            db_user = user

    user = list(user.items())
    db_user = list(user.items())

    update = {}

    for i in range(0,len(user)):
        if(user[i][1]!=db_user[i][1]):
            update[user[i][0]] = user[i][1]
            
    
    
    

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
            #member quant
            guild = self.bot.get_guild(743482187365613641)
            member_count = int(guild.member_count)
            #channels quant
            channel_count = len(guild.channels)
            #staff quant
            staff_count = 0


            #staffs and boosters
            staffs, boosters = [], [] # VAI RECEBER DADOS DO SERVER
            staffs_to_add, boosters_to_add = [], [] # VAI RECEBER STAFFS CASO NÃO ESTEJAM NO BANCO
            already_on = []
            try:
                db_staffs, db_boosters = await find_staff() # VAI RECEBER STAFFS DO BANCO
                def get_all_ids(lista):
                    for i in lista:
                        already_on.append(i['id'])
                get_all_ids(db_staffs)
                get_all_ids(db_boosters)
            except:
                print('erro')
                db_staffs, db_boosters = [], []

            staff_roles_names = ["⎯⎯⎯⎯⎯⎯⠀〔Admin's〕⎯⎯⎯⎯⎯⎯⎯⠀", "⎯⎯⎯⎯⎯⎯⎯⎯⠀〔Mod〕⎯⎯⎯⎯⎯⎯⎯⎯⎯⠀", '⎯⎯⎯⎯⎯⎯⠀〔Dono〕⎯⎯⎯⎯⎯⎯⎯⠀']
            role_types = {"⎯⎯⎯⎯⎯⎯⠀〔Admin's〕⎯⎯⎯⎯⎯⎯⎯⠀":"ADMIN", "⎯⎯⎯⎯⎯⎯⎯⎯⠀〔Mod〕⎯⎯⎯⎯⎯⎯⎯⎯⎯⠀":"MOD", "⎯⎯⎯⎯⎯⎯⠀〔Dono〕⎯⎯⎯⎯⎯⎯⎯⠀":"OWNER", "BOOSTER ❤️":"boosters"}
            for member in guild.members:
                for role in member.roles:
                    if role.name in staff_roles_names:
                        if member.id not in already_on:
                            staff_count += 1
                            role = role_types[member.top_role.name]
                            new_staffs.append({'id': member.id, 'name': member.name, 'pfp': str(member.avatar_url), 'bio':'Biografia Não Definida', 'ocupacao':'', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':role})
                        else:

                            



                            db_discord_member = {

                            }


                            get_update({
                                id: member.id,

                            }, {
                                id: ""
                            })
                            
                            

                    if role.name == "BOOSTER ❤️"  and member.id not in already_on:
                        new_boosters.append({'id': member.id, 'name': member.name, 'pfp': str(member.avatar_url), 'bio':'Biografia Não Definida', 'ocupacao':'', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':'BOOSTER'})
            

            


            print(f'''
            staffs: {staffs}
            boosters: {boosters}
            ''')
            #site.update_one({'_id':0}, {'$set':{'channel_count':channel_count, 'staff_count':staff_count, 'member_count':member_count, 'staffs':staffs, 'boosters':boosters}})

        get_info.start(self)

def setup(bot):
    bot.add_cog(Tarefas(bot))
