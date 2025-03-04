import os
import subprocess

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import openai

from app.config import settings

router = Router()


@router.message(CommandStart())
async def on_start(message: Message):
    await message.answer("Привет! Отправь мне голосовое сообщение и я его расшифрую 😊")


@router.message(F.voice)
async def voice_message(message: Message):
    voice = message.voice
    try:
        file = await message.bot.get_file(voice.file_id)

        os.makedirs("temp", exist_ok=True)

        ogg_path = os.path.join('temp', 'temp_voice.ogg')
        wav_path = os.path.join('temp', 'temp_voice.wav')

        await message.bot.download_file(file.file_path, ogg_path)

        try:
            subprocess.run([
                rf"{settings.FFMPEG_PATH}",
                "-i",
                ogg_path,
                wav_path
            ], check=True)
            print("✅ SUCCESS CONVERT ✅")
        except FileNotFoundError:
            err = 'CHECK FFMPEG PATH'
            print("⛔ CHECK FFMPEG PATH ⛔")
        except subprocess.CalledProcessError as e:
            err = e
            print(f"⛔ CONVERT ERROR: {e}")

        try:
            with open(wav_path, "rb") as audio_file:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
        except Exception as e:
            print(f"⛔ TRANSCRIPT ERROR: {e}")

        os.remove(ogg_path)
        os.remove(wav_path)

        await message.answer(response)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")