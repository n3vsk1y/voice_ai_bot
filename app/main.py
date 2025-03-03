import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.config import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TG_BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет!")


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("help работает")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print('✅ BOT STARTED ✅')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('⛔ BOT STOPPED ⛔')
