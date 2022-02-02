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
    info = site.find_one({'_id': 1})
    staffs = info['staffs']
    boosters = info['boosters']
    return [staffs, boosters]

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

            #staff quant
            staff_count = 0
            staffs = []
            boosters = []
            new_staffs = []
            new_boosters = []

            old_info = True
            already_on_staff = []
            staff_old_info = {}
            booster_old_info = {}
            try:
                for category in await find_staff():
                    for member in category:
                        already_on.append(member['id'])
                        if member['role'] == 'BOOSTER':
                            booster_old_info[{'id':member.id, 'info':member}]
                        else:
                            staff_old_info[{'id':member.id, 'info':member}]
            except:
                old_info = False
                pass



            staff_roles_names = ["⎯⎯⎯⎯⎯⎯⠀〔Admin's〕⎯⎯⎯⎯⎯⎯⎯⠀", "⎯⎯⎯⎯⎯⎯⎯⎯⠀〔Mod〕⎯⎯⎯⎯⎯⎯⎯⎯⎯⠀", '⎯⎯⎯⎯⎯⎯⠀〔Dono〕⎯⎯⎯⎯⎯⎯⎯⠀']
            role_types = {"⎯⎯⎯⎯⎯⎯⠀〔Admin's〕⎯⎯⎯⎯⎯⎯⎯⠀":"ADMIN", "⎯⎯⎯⎯⎯⎯⎯⎯⠀〔Mod〕⎯⎯⎯⎯⎯⎯⎯⎯⎯⠀":"MOD", "⎯⎯⎯⎯⎯⎯⠀〔Dono〕⎯⎯⎯⎯⎯⎯⎯⠀":"OWNER", "BOOSTER ❤️":"boosters"}
            for member in guild.members:
                for e in member.roles:
                    if e.name in staff_roles_names and member.id not in already_on_staff:
                        staff_count += 1
                        role = role_types[member.top_role.name]
                        new_staffs.append({'id': member.id, 'name': member.name, 'pfp': str(member.avatar_url), 'bio':'Biografia Não Definida', 'ocupacao':'', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':role})
                        staffs.append(member)
                    if e.name == "BOOSTER ❤️" and member.id not in already_on_staff:
                        staff_count += 1
                        new_boosters.append({'id': member.id, 'name': member.name, 'pfp': str(member.avatar_url), 'bio':'Biografia Não Definida', 'ocupacao':'', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':'BOOSTER'})
                        boosters.append(member)
            #channels quant
            channel_count = len(guild.channels)

            #verify if name or pfp changed
            if old_info:
                role_list = [[staffs, boosters], [[staff_old_info, new_staffs], [booster_old_info, new_boosters]]] #0 = staff, 1 = booster
                for e in range(2):
                    for member in role_list[0][e]:
                        for i in ['name', 'pfp']:
                            if role_list[1][e][0][member.id]['info'][i] != member.name:
                                print(f'Nome ou pfp de {member.name} mudou')
                                role_list[1][e][0][member.id]['info'][i] = member.name
                                role_list[1][e][1].append(role_list[1][e][0][member.id]['info'])
            
            #push info to site collection
            print('PUSHING INFO TO MONGO')
            site.find_one_and_update({'_id': 1}, {'$set': {'member_count': member_count, 'staff_count': staff_count, 'channel_count': channel_count}})
            if len(new_staffs) + len(new_boosters) > 0:
                print('NEW STAFF FOUND')
                def update_members_db(members, type):
                    for new in members:
                        site.find_one_and_update({'_id': 1}, {'$push': {type: new}})
                update_members_db(new_staffs, 'staffs')
                update_members_db(new_boosters, 'boosters')
                print('NEW STAFF PUSHED')
            print('INFO PUSHED')
        get_info.start(self)

def setup(bot):
    bot.add_cog(Tarefas(bot))
