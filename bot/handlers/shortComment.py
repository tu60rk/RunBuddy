from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup

# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils.exceptions import ChatNotFound

from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from sqlalchemy.ext.asyncio import AsyncSession

from db.request import (
    getUserRegistrationId,
    getMaxDateMeet,
    getIdMeetLastMeet,
    getMeetById,
    updateMeetData,
)
from settings.config import textBotSettings

# from utils.buttons import (
#     # createMainMenu,
#     # createBinaryAnswer,
#     # getListBinaryAnswer,
# )
# from utils.bd import DataBase
# from settings.config import botMainSettings, botTextSettings

# waitGetComment = botMainSettings.waitGetComment
# menuText = botTextSettings.menuText.replace("|", "\n")
# exceptionText = botTextSettings.exceptionText.replace("|", "\n")

# db = DataBase()

# set way of change registration
# class getCommentShort(StatesGroup):
#     shortComment = State()

router = Router()


async def updateMeetDataF(session: AsyncSession, idTelegram: str):
    # idUser = await db.getUserRegistrationId(idTelegram=idTelegram)
    # idMeet = await db.getIdMeetLastMeet(idUser=idUser)

    # whichUser = await db.whichUserInMeet(meetId=idMeet, userId=idUser)
    # columnName = "first_partner_meet"
    # if whichUser == 1:
    #     columnName = "second_partner_meet"

    # await db.updateMeetData(meetId=idMeet, columnName=columnName, data=result)
    idUser = await getUserRegistrationId(session=session, idTelegram=idTelegram)
    maxDateMeet = await getMaxDateMeet(session=session)
    idMeet = await getIdMeetLastMeet(
        session=session, idUser=idUser, maxDateMeet=maxDateMeet
    )
    meet = await getMeetById(session=session, meetId=idMeet, use_pandas=True)
    whichUser = 2
    if not meet[meet.idUserOne == idUser].empty:
        whichUser = 1

    columnName = "first_partner_meet"
    if whichUser == 1:
        columnName = "second_partner_meet"

    await updateMeetData(
        session=session, meetId=idMeet, columnName=columnName, data=True
    )


# async def startGetShortComment(bot, idTelegram: str, dp) -> None:
#     @dp.async_task
#     async def start(bot, idTelegram: str, dp):
#         dp.set_current(dp)
#         state = dp.current_state(chat=idTelegram, user=idTelegram)

#         try:
#             await bot.send_message(
#                 idTelegram,
#                 botTextSettings.startShortComment,
#                 reply_markup=createBinaryAnswer(),
#             )
#         except TelegramNotFound:
#             pass
#         await state.set_state(getCommentShort.shortComment)
#         await asyncio.sleep(waitGetComment)
#         try:
#             data = await state.get_data()
#             if data["isFindPartnerNotExceed"] is True:
#                 pass
#         # Если пользователь не ответил или за это время state завершился, получаем KeyError и Сохраняем результат, что он встретился
#         except KeyError:
#             await updateMeetData(idTelegram=idTelegram, result=False)
#             menu = await createMainMenu(userId=idTelegram)
#             try:
#                 await bot.send_message(
#                     idTelegram, botTextSettings.notAnswerShortComment, reply_markup=menu
#                 )
#             except TelegramNotFound:
#                 pass
#             await state.finish()

#     await start(bot=bot, idTelegram=idTelegram, dp=dp)


@router.message(Command("meet_was"), StateFilter(default_state))
async def cmdShortComment(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    menu: ReplyKeyboardMarkup,
    botTextSettings: textBotSettings
) -> None:
    # if message.text not in getListBinaryAnswer():
    #     await message.answer(
    #         exceptionText,
    #         reply_markup=createBinaryAnswer(),
    #     )
    #     return
    # await state.update_data(isFindPartnerNotExceed=True)
    # await updateMeetDataF(
    #     session=session,
    #     idTelegram=message.from_user.id,
    #     # result=True if message.text == "Да" else False,
    # )
    # menu = await createMainMenu(userId=message.from_user.id)
    # if customer block us
    # try:
    #     await message.answer(
    #         (
    #             botTextSettings.positiveAnswerOfShortComment
    #             if message.text == "Да"
    #             else botTextSettings.negativeAnswerOfShortComment
    #         ),
    #         reply_markup=menu,
    #     )
    # except TelegramNotFound:
    #     pass
    # await asyncio.sleep(waitGetComment)
    # await state.finish()
    await updateMeetDataF(
        session=session,
        idTelegram=message.from_user.id,
    )

    await message.answer(
        (
            botTextSettings.positiveAnswerOfShortComment
            if message.text == "Да"
            else botTextSettings.negativeAnswerOfShortComment
        ),
        reply_markup=menu,
    )
    await state.clear()


# def registerHandlersGetShortComments(dp: Dispatcher) -> None:
#     dp.register_message_handler(cmdShortComment, state=getCommentShort.shortComment)
