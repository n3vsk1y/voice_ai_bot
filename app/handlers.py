import os
import subprocess

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

import openai

from app.config import settings
from app.gpt import generate_speech, get_assistant_response

router = Router()


@router.message(CommandStart())
async def on_start(message: Message):
    await message.answer("Привет! Задай мне вопрос, на который я смогу ответить, или отправь голосовое сообщение и я его расшифрую 😊")


@router.message(F.voice)
async def voice_message(message: Message):
    wait_message = await message.answer("⏳ Думаю...")
    voice = message.voice
    try:
        if not os.path.exists(settings.FFMPEG_PATH):
            print(f"⛔ FFmpeg не найден по пути: {settings.FFMPEG_PATH}")

        file = await message.bot.get_file(voice.file_id)

        os.makedirs("temp", exist_ok=True)

        ogg_path = os.path.join("temp", f"{message.from_user.id}.ogg")
        wav_path = os.path.join("temp", f"{message.from_user.id}.wav")

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
            print("⛔ CHECK FFMPEG PATH ⛔")
        except subprocess.CalledProcessError as e:
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

        try:
            if not response.strip():
                raise ValueError
            
            text_response = await get_assistant_response(response)
            audio_path = await generate_speech(text_response)

            await wait_message.delete()
            
            if audio_path:
                voice_file = FSInputFile(audio_path)
                await message.reply_voice(voice=voice_file)
                os.remove(audio_path)
            else:
                await message.answer(text_response)

        except ValueError:
            print("⛔ EMPTY QUESTION ⛔")
        except Exception as e:
            print(f"⛔ GPT ERROR: {e}")

    except Exception as e:
        await message.answer(f"⛔ Ошибка: {e}")
