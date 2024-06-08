from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from utils.buttons import createMainMenu
from utils.bd import DataBase

db = DataBase()

# echo handler function
async def startCommandHandler(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    menu = await createMainMenu(userId=message.from_user.id)
    await message.reply(
        """Привет!👋
Это команда Run Buddy — бота для нетворкинга на бегу. Мы поможем найти с кем тебе побегать, познакомим с новыми людьми, а новичкам поможем влиться в беговую тусовку!

Каждый понедельник бот будет присылать случайного человека для пробежки — вам останется только связаться друг с другом и договориться об удобной дате.

Но сначала нужно зарегистрироваться, чтобы мы узнали тебя получше и смогли подобрать пару для пробежки. Нажимай на кнопку и начнём!""",
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
