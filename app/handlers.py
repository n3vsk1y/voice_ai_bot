import os
import subprocess
import uuid
import logging

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

import openai

from app.config import settings
from app.assistant import generate_speech, get_assistant_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI BOT")

router = Router()


@router.message(CommandStart())
async def on_start(message: Message):
    await message.answer("Привет! Задай мне вопрос в голосовом сообщении! 🎙️")


@router.message(F.voice)
async def voice_message(message: Message):
    wait_message = await message.answer("⏳ Думаю...")
    file = await message.bot.get_file(message.voice.file_id)

    filename = str(uuid.uuid4())
    ogg_path = os.path.join("temp", f"{filename}.ogg")
    wav_path = os.path.join("temp", f"{filename}.wav")

    os.makedirs("temp", exist_ok=True)
    await message.bot.download_file(file.file_path, ogg_path)

    try:
        subprocess.run([
            settings.FFMPEG_PATH, "-i", ogg_path, wav_path
        ], check=True)
        logger.info("✅ SUCCESS CONVERT ✅")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        logger.error(f"⛔ FFmpeg ERROR: {e}")
        await wait_message.delete()
        return await message.answer("⛔ Ошибка конвертации аудио.")

    try:
        with open(wav_path, "rb") as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
    except Exception as e:
        logger.error(f"⛔ TRANSCRIPTION ERROR: {e}")
        await wait_message.delete()
        return await message.answer("⛔ Ошибка расшифровки аудио")

    if not response.strip():
        logger.warning("⛔ EMPTY QUESTION ⛔")
        await wait_message.delete()
        return await message.answer("⛔ Голосовое сообщение пустое")

    try:
        text_response = await get_assistant_response(message.from_user.id, response)
        audio_path = await generate_speech(text_response, filename)
    except Exception as e:
        logger.error(f"⛔ GPT ERROR: {e}")
        await wait_message.delete()
        return await message.answer("⛔ Ошибка обработки текста")

    await wait_message.delete()

    if audio_path:
        voice_file = FSInputFile(audio_path)
        await message.reply_voice(voice=voice_file)
        os.remove(audio_path)
    else:
        await message.answer(text_response)

    os.remove(ogg_path)
    os.remove(wav_path)
