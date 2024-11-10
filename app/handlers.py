from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from parsing import download_and_generate_schedule
from app.keyboards_Reply import verification
import app.keyboards_Inline as kb


router = Router()

@router.message(CommandStart())
async def message_handler(message: types.Message):
    await message.reply("Из какой вы группы?", reply_markup=kb.inline_kb1)

@router.callback_query(F.data.startswith('btn_'))
async def process_order_callback(callback_query: CallbackQuery):
    name_group = callback_query.data.split('_')[1]
    await callback_query.message.answer(f"Ваша группа {name_group}?", reply_markup=verification())
    await callback_query.answer()
    group_user = [name_group]
    print(group_user)

# @router.message(F.text == 'Да')
# async def yes(message: types.Message):


@router.message(F.text == 'Рас')
async def get_photo(message: types.Message):
    file_path = download_and_generate_schedule()
    await message.reply_photo(
        photo=types.FSInputFile(
            path=file_path,
        ),
    )

if __name__ == "__main__":
    from aiogram.utils import executor
    executor.start_polling(router, skip_updates=True)