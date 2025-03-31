from aiogram import Dispatcher, types, F, Router

# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text

# from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.utils.formatting import Text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.request import (
    isCanGetComment,
    insertCommonComment,
    getMeetStatus,
)
from utils.buttons import createMainMenu

# from utils.bd import DataBase
from settings.config import botTextSettings

# db = DataBase()
router = Router()
botStartText = botTextSettings.botStartText.replace("|", "\n")
commentTextInputException255 = botTextSettings.commentTextInputException255


class comment(StatesGroup):
    stateComment = State()


async def sendNotification(bot, idTelegram, text):
    await bot.send_message(idTelegram, text)


@router.message(CommandStart(), StateFilter(default_state))
async def startCommandHandler(
    message: types.Message, session: AsyncSession, admins: List
) -> None:
    # await state.finish()
    menu = await createMainMenu(
        userId=message.from_user.id, session=session, admins=admins
    )
    await message.reply(
        botStartText,
        reply_markup=menu,
    )


# Накинуть middleware!
@router.message(F.text == "Оставить отзыв", StateFilter(default_state))
async def writeComment(
    message: types.Message, state: FSMContext, session: AsyncSession, admins: List
) -> None:
    # await state.finish()
    # if await db.isCanGetComment(userId=message.from_user.id, session=session):
    if await isCanGetComment(userId=message.from_user.id, session=session):
        await message.answer(
            botTextSettings.stayComment,
            reply_markup=types.ReplyKeyboardRemove(),
        )
        # await comment.stateComment.set()
        await state.set_state(comment.stateComment)
    else:
        menu = await createMainMenu(
            userId=message.from_user.id, session=session, admins=admins
        )
        await message.answer(
            botTextSettings.stayCommentExeption,
            reply_markup=menu,
        )


@router.message(StateFilter(comment.stateComment))
async def cmdStateComment(
    message: types.Message, state: FSMContext, session: AsyncSession, admins: List
) -> None:
    if len(message.text) > 255:
        await message.answer(commentTextInputException255)
        return

    # await db.insertCommonComment(
    #     id_telegram=str(message.from_user.id), comment=message.text
    # )
    await insertCommonComment(
        session=session, id_telegram=str(message.from_user.id), comment=message.text
    )
    menu = await createMainMenu(
        userId=message.from_user.id, session=session, admins=admins
    )
    await message.answer(
        botTextSettings.stayCommentFinish,
        reply_markup=menu,
    )
    # await state.finish()
    await state.clear()


@router.message(F.text == "Узнать мой статус по встречам", StateFilter(default_state))
async def checkStatus(
    message: types.Message, state: FSMContext, session: AsyncSession, admins: List
) -> None:
    menu = await createMainMenu(
        userId=message.from_user.id, session=session, admins=admins
    )
    # meetStatus = await db.getMeetStatus(userId=message.from_user.id)
    meetStatus = await getMeetStatus(userId=message.from_user.id)
    await message.reply(
        f"""Статус по встречам - {'Активный' if meetStatus[0][0] == True else 'Не активный'}""",
        reply_markup=menu,
    )
    # await state.finish()
    await state.clear()


# def registerHandlersCommon(dp: Dispatcher) -> None:
# dp.register_message_handler(startCommandHandler, commands="start", state="*")
# dp.register_message_handler(
#     checkStatus,
#     Text(equals=["Узнать мой статус по встречам"], ignore_case=True),
#     state="*",
# )
# dp.register_message_handler(
#     writeComment,
#     Text(equals=["Оставить отзыв"], ignore_case=True),
#     state="*",
# )
# dp.register_message_handler(cmdStateComment, state=comment.stateComment)
