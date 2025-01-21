import asyncio

from app.get_photo import run_scheduler
from create_bot import bot, dp
from app import start_router, answer_button_router,  get_photo_router, yes_handler_router




async def main():
    dp.include_routers(
        start_router,
        answer_button_router,
        get_photo_router,
        yes_handler_router
    )
    polling_task = asyncio.create_task(dp.start_polling(bot))
    scheduler_task = asyncio.create_task(run_scheduler())

    await asyncio.gather(polling_task, scheduler_task)

    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())



if __name__ == "__main__":
    asyncio.run(main())
