import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from pydub import AudioSegment

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

        ogg_path = os.path.join('temp', 'temp_voice.ogg')
        wav_path = os.path.join('temp', 'temp_voice.wav')

        await message.bot.download_file(file.file_path, ogg_path)

        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(wav_path, format="wav")

        await message.answer(f"Расшифровка:")

        # Удаляем временные файлы
        os.remove(ogg_path)
        os.remove(wav_path)

    except Exception as e:
        await message.answer("Ошибка при сохранении голосового сообщения")
        print(f"Ошибка: {e}")
