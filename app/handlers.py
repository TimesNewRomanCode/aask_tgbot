from aiogram import Router, F, types
from aiogram.filters import CommandStart
from parsing import download_and_generate_schedule
import app.keyboards as kb


router = Router()

@router.message(CommandStart())
async def message_handler(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)


@router.message(F.text == '4')
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