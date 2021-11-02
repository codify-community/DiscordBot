from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import asyncio
import json
import nest_asyncio
from aiogram.types.message import ContentType
from config import config
from aiohttp import ClientSession
loop = asyncio.new_event_loop()


async def sendMessage(bot, message: Message, text=None):
    photos = await bot.get_user_profile_photos(message.from_user.id)

    # message.reply_to_message
    t = (text or message.text).replace('@everyone', 'eu sou gay, a culpa eh do meu pai').replace('@here',
                                                                                                 'que contratou um tal de Wilson para ser o capatras, eu vi o bob tomar banho e vi o tamanho da sua mala, falei pra ele vai de vagar amor, ainda sou moça e nao quero sentir dor')

    content = t if message.reply_to_message is None else f'respondendo á **{message.reply_to_message.from_user.first_name} {message.reply_to_message.from_user.last_name or ""}**\n> {message.reply_to_message.text or "*mensagem não suportada*"}\n{t}'
    if photos.photos == None or len(photos.photos) == 0:
        async with ClientSession() as session:
            _ = await session.post(config().discordWebhookUrl, data=json.dumps({
                "username": f"{message.from_user.first_name} {message.from_user.last_name or ''}"[:32],
                "avatar_url": None,
                "content": content,
            }), headers={"Content-Type": "application/json"})
        return
    file = await bot.get_file(photos.photos[0][0].file_id)

    async with ClientSession() as session:
        photo = await file.get_url()
        _ = await session.post(config().discordWebhookUrl, data=json.dumps({
            "username": f"{message.from_user.first_name} {message.from_user.last_name or ''}"[:32],
            "avatar_url": photo,
            "content": content,
        }), headers={"Content-Type": "application/json"})
bot = Bot(token=config().telegramToken)
dp = Dispatcher(bot)


def main():
    nest_asyncio.apply(loop)
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, skip_updates=True,
                           loop=loop)
    


@dp.message_handler(content_types=ContentType.ANY)
async def onMessage(message: Message):
    if message.sticker is not None:
        sticker_url = await bot.get_file(message.sticker.file_id)
        url = await sticker_url.get_url()
        return await sendMessage(bot, message, url if not url.endswith('.tgs') else '*mensagem não suportada.*')
    elif message.photo is not None and len(message.photo) > 0:
        photo = message.photo.pop()
        await sendMessage(bot, message, await photo.get_url() if photo.file_size < 8e+6 else f'*imagem muito grande. {photo.file_size*1e+6}mb.')
        if message.caption is not None:
            await sendMessage(bot, message, message.caption)
    elif message.video is not None or message.audio is not None or message.document is not None:
        attach = message.video or message.audio or message.document
        await sendMessage(bot, message, await attach.get_url() if attach.file_size < 8e+6 else f'*arquivo muito grande. {attach.file_size*1e+6}mb.')
        if message.caption is not None:
            await sendMessage(bot, message, message.caption)
        pass
    else:
        return await sendMessage(bot, message)

if __name__ == '__main__':
    main()
