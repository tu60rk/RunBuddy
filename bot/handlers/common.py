from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.buttons import createMainMenu
from utils.bd import DataBase
from settings.config import botTextSettings

db = DataBase()
botStartText = botTextSettings.botStartText.replace("|", "\n")
commentTextInputException255 = botTextSettings.commentTextInputException255

class comment(StatesGroup):
    stateComment = State()


async def sendNotification(bot, idTelegram, text):
    await bot.send_message(idTelegram, text)


async def startCommandHandler(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    menu = await createMainMenu(userId=message.from_user.id)
    await message.reply(
        botStartText,
        reply_markup=menu,
    )

async def writeComment(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    if await db.isCanGetComment(userId=message.from_user.id):
        await message.answer(
            "Напиши свой отзыв",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await comment.stateComment.set()
    else:
        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            "Ты не сможешь оставить отзыв, пока не зарегистрируешься и не поучавствуешь в 1 встрече.",
            reply_markup=menu,
        )

async def cmdStateComment(message: types.Message, state: FSMContext) -> None:
    if message.text > 255 and len(message.text) < 5:
        await message.answer(commentTextInputException255)
        return

    await db.insertCommonComment(
        id_telegram=message.from_user.id,
        comment=message.text
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
        "Спасибо за Ваш отзыв!",
        reply_markup=menu,
    )
    await state.finish()

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
    dp.register_message_handler(
        writeComment,
        Text(equals=["Оставить отзыв"], ignore_case=True),
        state="*",
    )
    dp.register_message_handler(cmdStateComment, state=comment.stateComment)
