# from aiogram import Router, F, types
# from aiogram.client import bot
# from aiogram.filters import CommandStart, callback_data, state
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery
# from aiogram.utils.formatting import Text
# from pydantic import BaseModel
# from parsing import download_and_generate_schedule
# import app.keyboards_Reply as kb
# from aiogram.fsm.state import State, StatesGroup
#
# router = Router()
#
# @router.message(F.text == 'Да')
# async def yes(message: types.Message):
#
#
#
# if __name__ == "__main__":
#     from aiogram.utils import executor
#     executor.start_polling(router, skip_updates=True)