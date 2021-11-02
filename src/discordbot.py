import asyncio
import logging
from discord import Message
from config import config
from telegram.utils.helpers import escape_markdown
from discord import Client
from tgbot import bot as TgBot, loop as TgLoop
BotConfig = config()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
async def sendMessage(text):
    async def inner():
        s_msg_task = TgBot.send_message(chat_id=BotConfig.telegramChannelId, text=text, parse_mode='markdownv2')
        asyncio.run_coroutine_threadsafe(s_msg_task, TgLoop).result()
    task = asyncio.create_task(inner())
    await task
class CodifyBot(Client):
    def __init__(self, token):
        super().__init__()
        self.token = token
       
        
    # def setupCommands(self):
    #     logging.info("Loading commands...")
    #     self.load_extension("commands.helper")
    #     logging.info("loaded helper command")
    
    async def on_message(self, message: Message):
        if 905056728889032764 == message.author.id:
            return
        if message.author.id == self.user.id:
            return
        if message.channel.id == BotConfig.OffTopicChannelId:
            if message.reference is not None:
                ref_message = await message.channel.fetch_message(message.reference.message_id)       
                NL = '\n'
                T = '\t'
                user = '<unknown>'
                try:
                    user = message.author.nick or ref_message.author.name
                except:
                    user = message.author.name
                b = '» '
                s = f"respondendo á **{user}** {NL}{T}{f'{b}'.join(ref_message.content.split(NL)).strip() if NL in ref_message.content else f'{b} {ref_message.content.strip()}'}\n[{message.author.nick or message.author.name}]  {message.content}"
                await sendMessage(escape_markdown(s.strip(), 2))
                return
            a = '\['
            b = '\]'
            user = None
            try:
                user = ref_message.author.nick or ref_message.author.name
            except:
                user = ref_message.author.name
            await sendMessage(escape_markdown(f'[{user}]  {message.content}', 2))
    def botRun(self):
        #self.setupCommands()
        self.run(self.token)


bot = CodifyBot(BotConfig.token)


def main():
    bot.botRun()

if __name__ == "__main__":
    main()
