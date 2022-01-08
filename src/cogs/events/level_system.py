import logging
import random

from discord import Bot, Message, Embed
from discord import Cog as Extension
from discord.ext import tasks

from src.accounts.users import DataBaseUser


def count_repeated_words(string) -> dict[str, int]:
    dic = dict()
    words = string.split()
    for raw_word in words:
        word = raw_word.lower()
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    return dic


def get_major_item_in_a_dict(dic):
    kv = ["", 0]
    for value, key in enumerate(dic):
        int_val = int(dic[key])
        if int_val >= kv[1]:
            kv = [key, int_val]
    return kv


class LevelSystem(Extension):
    def __init__(self, bot: Bot):
        self.logger = logging.getLogger(__name__)
        self.levelUpChannel = None
        self.bot = bot
        self.add_xp_queue = []

    @tasks.loop(seconds=30)
    async def update_xp(self):
        while True:
            try:
                user = self.add_xp_queue.pop()
                db_user = DataBaseUser(user['id'])
                up = await db_user.increase_xp_by(user['xp'])
                print("Added {} xp to {}".format(user['xp'], user['id']))
                level = await db_user.get_level()
                if up:
                    embed = Embed(title="Level Up!", color=0x738ADB)
                    embed.description = f"GG! <@{user['id']}> upou para o level {level}!"
                    u = self.bot.get_user(user['id'])
                    if u:
                        embed.set_thumbnail(url=u.avatar.url)
                    await self.levelUpChannel.send(embed=embed)
            except IndexError:
                break

    @Extension.listener()
    async def on_ready(self):
        self.update_xp.start()
        self.levelUpChannel = self.bot.get_channel(929392775366049832)

    @Extension.listener()
    async def on_message(self, message: Message):
        if not message.author.bot:
            most_repeated_word_in_message = get_major_item_in_a_dict(count_repeated_words(message.content))
            self.logger.debug(f"Removing {most_repeated_word_in_message[1]} XP from message with is "
                              f"{most_repeated_word_in_message[0]}")
            obj = {
                "id": message.author.id,
                "xp": random.randint(1, 10) + len(message.content) if len(message.content) < 32
                else random.randint(1, 32) + message.content.count(' ') - len(most_repeated_word_in_message[0])
                if most_repeated_word_in_message[1] > 1 else 0
            }
            self.add_xp_queue.append(obj) if obj not in self.add_xp_queue else None


def setup(bot: Bot):
    bot.add_cog(LevelSystem(bot))
