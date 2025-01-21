# get_photo.py

import asyncio
from datetime import datetime, time, timedelta
from aiogram import Router, types, F
from Database.db import Database
from parsing import download_and_generate_schedule
from create_bot import bot

get_photo_router = Router()

@get_photo_router.message(F.text == 'Да1')
async def get_photo(message: types.Message = None):
    """Обработчик команды 'Да1'."""
    print("Команда 'Да1' получена")
    db = Database()
    try:
        async with db:
            group_ids = await db.get_all_group_ids()
            for group in group_ids:
                chat_id = group["chat_id"]
                group_name = group["group_name"]
                file_path = download_and_generate_schedule(group_name)

                try:
                    await bot.send_photo(chat_id, types.FSInputFile(file_path))
                    print(f"Расписание для группы {group_name} отправлено в чат {chat_id}.")
                except Exception as e:
                    print(f"Ошибка при отправке расписания для группы {group_name}: {e}")
    except Exception as e:
        print(f"Ошибка при получении данных из базы: {e}")

async def scheduled_task():
    """Задача отправки расписания в определённое время."""
    print("Запуск задачи...")

    target_time = time(18, 30)
    now = datetime.now()
    next_run = datetime.combine(now.date(), target_time)

    print(f"Текущее время: {now}, время запуска: {next_run}")

    if next_run < now:
        next_run = datetime.combine((now + timedelta(days=1)).date(), target_time)

    delay = (next_run - now).total_seconds()
    print(f"Задача начнётся через {delay} секунд.")

    await asyncio.sleep(delay)

    # Подключение к базе данных и отправка сообщений по группам
    db = Database()
    try:
        async with db:
            group_ids = await db.get_all_group_ids()
            for group in group_ids:
                chat_id = group["chat_id"]
                group_name = group["group_name"]
                file_path = download_and_generate_schedule(group_name)

                try:
                    await bot.send_photo(chat_id, types.FSInputFile(file_path))
                    print(f"Расписание для группы {group_name} отправлено в чат {chat_id}.")
                except Exception as e:
                    print(f"Ошибка при отправке расписания для группы {group_name}: {e}")
    except Exception as e:
        print(f"Ошибка при получении данных из базы: {e}")

async def run_scheduler():
    """Запуск планировщика."""
    while True:
        await scheduled_task()
