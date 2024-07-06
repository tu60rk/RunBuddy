import io

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types.input_file import InputFile

from utils.buttons import createMainMenu
from utils.bd import DataBase
from settings.config import botTextSettings

db = DataBase()
botAdminText = botTextSettings.menuForAdmins.split("|")


async def getRegisteredPeoople(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    if db.isAdmin(userId=message.from_user.id):
        df = await db.getRegisteredUsers()
        df.to_excel("registeredUsers.xlsx")
        towrite = io.BytesIO()
        towrite.seek(0)
        text_file = InputFile(towrite, filename="registeredUsers.xlsx")
        await message.answer_document(
            text_file,
            reply_markup=types.ReplyKeyboardRemove(),
        )

    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
        botTextSettings.menuText,
        reply_markup=menu,
    )
    await state.finish()


async def getMeets(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    if db.isAdmin(userId=message.from_user.id):
        df = await db.getMeets()
        towrite = io.BytesIO()
        towrite.seek(0)
        text_file = InputFile(towrite, filename="meets.xlsx")
        await message.answer_document(
            text_file,
            reply_markup=types.ReplyKeyboardRemove(),
        )

    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
        botTextSettings.menuText,
        reply_markup=menu,
    )
    await state.finish()


def registerHandlersAdmin(dp: Dispatcher) -> None:
    dp.register_message_handler(
        getRegisteredPeoople,
        Text(equals=[botAdminText[0]], ignore_case=True),
        state="*",
    )
    dp.register_message_handler(
        getMeets,
        Text(equals=[botAdminText[1]], ignore_case=True),
        state="*",
    )
