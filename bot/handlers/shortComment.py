import asyncio

from aiogram import Dispatcher, types

# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils.exceptions import ChatNotFound

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNotFound


from utils.buttons import (
    createMainMenu,
    createBinaryAnswer,
    getListBinaryAnswer,
)
from utils.bd import DataBase
from settings.config import botMainSettings, botTextSettings

waitGetComment = botMainSettings.waitGetComment
menuText = botTextSettings.menuText.replace("|", "\n")
exceptionText = botTextSettings.exceptionText.replace("|", "\n")

db = DataBase()

# set way of change registration
class getCommentShort(StatesGroup):
    shortComment = State()


async def updateMeetData(idTelegram: str, result: bool):
    idUser = await db.getUserRegistrationId(idTelegram=idTelegram)
    idMeet = await db.getIdMeetLastMeet(idUser=idUser)

    whichUser = await db.whichUserInMeet(meetId=idMeet, userId=idUser)
    columnName = "first_partner_meet"
    if whichUser == 1:
        columnName = "second_partner_meet"

    await db.updateMeetData(meetId=idMeet, columnName=columnName, data=result)


async def startGetShortComment(bot, idTelegram: str, dp) -> None:
    @dp.async_task
    async def start(bot, idTelegram: str, dp):
        dp.set_current(dp)
        state = dp.current_state(chat=idTelegram, user=idTelegram)

        try:
            await bot.send_message(
                idTelegram,
                botTextSettings.startShortComment,
                reply_markup=createBinaryAnswer(),
            )
        except TelegramNotFound:
            pass
        await state.set_state(getCommentShort.shortComment)
        await asyncio.sleep(waitGetComment)
        try:
            data = await state.get_data()
            if data["isFindPartnerNotExceed"] is True:
                pass
        # Если пользователь не ответил или за это время state завершился, получаем KeyError и Сохраняем результат, что он встретился
        except KeyError:
            await updateMeetData(idTelegram=idTelegram, result=False)
            menu = await createMainMenu(userId=idTelegram)
            try:
                await bot.send_message(
                    idTelegram, botTextSettings.notAnswerShortComment, reply_markup=menu
                )
            except TelegramNotFound:
                pass
            await state.finish()

    await start(bot=bot, idTelegram=idTelegram, dp=dp)


async def cmdShortComment(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            exceptionText,
            reply_markup=createBinaryAnswer(),
        )
        return
    await state.update_data(isFindPartnerNotExceed=True)
    await updateMeetData(
        idTelegram=message.from_user.id, result=True if message.text == "Да" else False
    )
    menu = await createMainMenu(userId=message.from_user.id)
    # if customer block us
    try:
        await message.answer(
            botTextSettings.positiveAnswerOfShortComment
            if message.text == "Да"
            else botTextSettings.negativeAnswerOfShortComment,
            reply_markup=menu,
        )
    except TelegramNotFound:
        pass
    await asyncio.sleep(waitGetComment)
    await state.finish()


def registerHandlersGetShortComments(dp: Dispatcher) -> None:
    dp.register_message_handler(cmdShortComment, state=getCommentShort.shortComment)
