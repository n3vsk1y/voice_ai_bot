import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def on_start(message: Message):
    await message.answer("Привет! Отправь мне голосовое сообщение и я его расшифрую 😊")


@router.message(F.voice)
async def voice_message(message: Message):
    voice = message.voice
    try:
        file = await message.bot.get_file(voice.file_id)

        os.makedirs('temp', exist_ok=True)
        save_path = os.path.join('temp', 'temp_voice.ogg')
        await message.bot.download_file(file.file_path, save_path)

        os.remove(save_path)

    except Exception as e:
        await message.answer("Ошибка при сохранении голосового сообщения")
        print(f"Ошибка: {e}")
