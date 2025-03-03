import asyncio

from aiogram import Bot, Dispatcher

from app.handlers import router
from app.config import settings


async def main():
    bot = Bot(token=settings.TG_BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print('✅ BOT STARTED ✅')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('⛔ BOT STOPPED ⛔')
