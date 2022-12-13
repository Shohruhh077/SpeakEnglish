"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
from aiogram import Bot, Dispatcher, executor, types

from oxfordlookup import getDefinitions
from googletrans import Translator
translator = Translator()


API_TOKEN = '5947198285:AAEM6jz9B0NLsc0R-o5mS3M_hEwKVmjGB2o'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#1-handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Salom, \nMen Oksford izohli lug'at Botiman")

#2-handler
@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("☝️Mendan to'g'ri foydalanish: "
                        "\n1. Har qanday tildagi gapni ingliz tiliga tarjima qilaman."
                        "\n2. Ingliz tildagi gapni o'zbek tiliga tarjima qilaman."
                        "\n3. Biror bir so'zni Oksford izohli lug'atidan topib beraman.")

#3-handler
@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang =='en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)