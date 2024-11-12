from datetime import time
import schedule
import schedule
from aiogram import Router, F, types
from aiogram.client import bot
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from app.db import Database
from parsing import download_and_generate_schedule
from app.keyboards_Reply import verification
import app.keyboards_Inline as kb


router = Router()

db = Database()


@router.message(CommandStart() or F.text == 'Нет')
async def message_handler(message: types.Message):
    await message.reply("Из какой вы группы?", reply_markup=kb.inline_kb1)
    global chat_id
    chat_id = message.chat.id


@router.callback_query(F.data.startswith('btn_'))
async def process_order_callback(callback_query: CallbackQuery):
    global group_name
    group_name = callback_query.data.split('_')[1]
    await callback_query.message.answer(f"Ваша группа {group_name}?", reply_markup=verification())
    await callback_query.answer()

@router.message(F.text == 'Да')
async def yes(message: types.Message):
    print(group_name, chat_id)
    await message.answer("Теперь вы будуте получать расписание своей группы")
    async with db:
        await db.add_contact(chat_id, group_name)

@router.message()
async def get_photo(message: types.Message = None):
    file_path = download_and_generate_schedule()
    await message.reply_photo(
        photo=types.FSInputFile(
            path=file_path,
        ),
    )

if __name__ == "__main__":
    from aiogram.utils import executor
    executor.start_polling(router, skip_updates=True)