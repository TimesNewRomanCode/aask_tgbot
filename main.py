import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from os import getenv
from dotenv import load_dotenv

load_dotenv()
async def main():
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот работает")
