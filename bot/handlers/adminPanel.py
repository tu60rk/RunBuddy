from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.input_file import InputFile

from utils.buttons import createMainMenu
from utils.bd import DataBase
from settings.config import botTextSettings, botMainSettings

db = DataBase()
botAdminText = botTextSettings.menuForAdmins.split("|")
bot = Bot(token=botMainSettings.TELEGRAM_TOKEN)

class admin(StatesGroup):
    sendMessage = State()


async def getRegisteredPeoople(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    if db.isAdmin(userId=message.from_user.id):
        df = await db.getRegisteredUsers()
        pathFile = botMainSettings.path + botMainSettings.fileNameRegistered
        df.to_excel(pathFile)
        text_file = InputFile(pathFile, filename=botMainSettings.fileNameRegistered)
        
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
        pathFile = botMainSettings.path + botMainSettings.fileNameMeets
        df.to_excel(pathFile)
        text_file = InputFile(pathFile, filename=botMainSettings.fileNameMeets)
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

async def getComments(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    if db.isAdmin(userId=message.from_user.id):
        df = await db.getComments()
        pathFile = botMainSettings.path + botMainSettings.fileNameComments
        df.to_excel(pathFile)
        text_file = InputFile(pathFile, filename=botMainSettings.fileNameComments)
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


async def preSendMessage(message: types.Message, state: FSMContext)-> None:
    await state.finish()
    if db.isAdmin(userId=message.from_user.id):
        await message.answer(
            "Введи любой текст, который хочешь отправить активным пользователям.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await admin.sendMessage.set()

    else:
        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            "Вам такая команда не доступна.",
            reply_markup=menu,
        )

async def cmdSendMessage(message: types.Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(
            "Ты ничего не ввел! Давай попробуем снова.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        return

    users = await db.getUsers()
    for row in users:
        user_id = row[0]
        active = row[1]
        try:
            await bot.send_message(user_id, message.text)
            if active != True:
                await db.setActive(user_id, True)
        except:
            await db.setActive(user_id, False)
    
    menu = await createMainMenu(userId=message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        "Успешно отправлено!",
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
    dp.register_message_handler(
        getComments,
        Text(equals=[botAdminText[2]], ignore_case=True),
        state="*",
    )
    dp.register_message_handler(
        preSendMessage,
        Text(equals=[botAdminText[3]], ignore_case=True),
        state="*",
    )
    dp.register_message_handler(cmdSendMessage, state=admin.sendMessage)
