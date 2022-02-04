import discord
from discord.ext import commands

from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=os.getenv('prefix'), case_insensitive=True, intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():

    print('@================@')
    print('     BOT ONLINE   ')
    print('@================@')

    for i in os.listdir('./cogs'):
        for e in os.listdir(f'./cogs/{i}'):
            if str(e).startswith('__py'):
                pass
            else:
                print('loaded ', e)
                bot.load_extension(f'cogs.{i}.{e[:-3]}')

    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Codify Community", type=3))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".help | discord.gg/MSr8SJfR4H", type=3))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Beta 0.0.1", type=3))
        await asyncio.sleep(30)

def _reload():
    for i in os.listdir('./cogs'):
        for e in os.listdir(f'./cogs/{i}'):
            if str(e).startswith('__py'):
                pass
            else:
                bot.unload_extension(f'cogs.{i}.{e[:-3]}')
                bot.load_extension(f'cogs.{i}.{e[:-3]}')
                print('reloaded ', e)

@bot.command()
async def reload(ctx):
    _reload()

bot.run(os.getenv('token'))
