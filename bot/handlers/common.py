from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from utils.buttons import createMainMenu
from utils.bd import DataBase
from settings.config import botTextSettings

db = DataBase()
botStartText = botTextSettings.botStartText.replace("|", "\n")


async def sendNotification(bot, idTelegram, text):
    await bot.send_message(idTelegram, text)


async def startCommandHandler(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    menu = await createMainMenu(userId=message.from_user.id)
    await message.reply(
        botStartText,
        reply_markup=menu,
    )


async def checkStatus(message: types.Message, state: FSMContext) -> None:
    menu = await createMainMenu(userId=message.from_user.id)
    meetStatus = await db.getMeetStatus(userId=message.from_user.id)
    await message.reply(
        f"""Статус по встречам - {'Активный' if meetStatus[0][0] == True else 'Не активный'}""",
        reply_markup=menu,
    )
    await state.finish()


def registerHandlersCommon(dp: Dispatcher) -> None:
    dp.register_message_handler(startCommandHandler, commands="start", state="*")
    dp.register_message_handler(
        checkStatus,
        Text(equals=["Узнать мой статус по встречам"], ignore_case=True),
        state="*",
    )
