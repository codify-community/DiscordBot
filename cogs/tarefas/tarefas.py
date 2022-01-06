import discord
from discord.ext import commands, tasks
import asyncio
import datetime
from utils.mongoconnect import mongoConnect
  
cluster = mongoConnect()
db = cluster['codify']
site = ['site']
logs = db['logs']

class Tarefas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @tasks.loop(hours=24)
        async def send_status():
            hr = datetime.datetime.now()
            logs.find_one_and_update({'_id': 0}, {'$set': {'last_ping': hr}})
        send_status.start()

        @tasks.loop(hours=24)
        async def get_info():
            #member quant
            guild = bot.get_guild(743482187365613641)
            member_count = int(guild.member_count)

            #staff quant
            staff_count = 0
            dono_ = bot.get_user(693639831443734538)
            dono = {'id': dono_.id, 'name': dono_.name, 'pfp': dono_.avatar_url, 'bio':'Biografia Não Definida', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':'OWNER'}
            admins = []
            mods = []
            boosters = []
            for member in guild.members:
                for e in member.roles:
                    if e.name == "⎯⎯⎯⎯⎯⎯⠀〔Admin's〕⎯⎯⎯⎯⎯⎯⎯⠀":
                        staff_count += 1
                        admins.append({'id': member.id, 'name': member.name, 'pfp': member.avatar_url, 'bio':'Biografia Não Definida', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':'ADMIN'})
                    if e.name == "⎯⎯⎯⎯⎯⎯⎯⎯⠀〔Mod〕⎯⎯⎯⎯⎯⎯⎯⎯⎯⠀":
                        staff_count += 1
                        mods.append({'id': member.id, 'name': member.name, 'pfp': member.avatar_url, 'bio':'Biografia Não Definida', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':'MOD'})
                    if e.name == "BOOSTER ❤️":
                        staff_count += 1
                        boosters.append({'id': member.id, 'name': member.name, 'pfp': member.avatar_url, 'bio':'Biografia Não Definida', 'habilidades':['Nenhuma'], 'github':'https://github.com/codify-community', 'role':'BOOSTER'})
            #channels quant
            channel_count = len(guild.channels)

            #push info to site collection
            site.find_one_and_update({'_id': 0}, {'$set': {'member_count': member_count, 'staff_count': staff_count, 'dono': dono, 'admins': admins, 'mods': mods, 'boosters':boosters, 'channel_count': channel_count}})
        get_info.start()

def setup(bot):
    bot.add_cog(Tarefas(bot))
