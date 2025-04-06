import uuid
from aiogram import Bot
from aiogram.exceptions import TelegramNotFound, TelegramBadRequest
from aiogram.types.input_file import FSInputFile, InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import List

# from aiogram.contrib.fsm_storage.base import StorageKey
# from aiogram.dispatcher import FSMContext


from utils.core import generalAlgoritm

# from utils.bd import admins

# from handlers.getComments import startGetComments
from db.request import (
    getMaxDateMeet,
    getLastMeet,
    getUsersWhichDontAnswer,
)

# from handlers.shortComment import startGetShortComment
# from handlers.common import sendNotification
from settings.config import botMainSettings, botTextSettings


# coreDayOfWeek = botMainSettings.coreDayOfWeek
# coreHour = botMainSettings.coreHour
# coreMinute = botMainSettings.coreMinute

# activateComments = botMainSettings.activateComments
# commentDayOfWeek = botMainSettings.commentDayOfWeek
# commentHour = botMainSettings.commentHour
# commentMinute = botMainSettings.commentMinute

# dontAnswerDayOfWeek = botMainSettings.dontAnswerDayOfWeek
# dontAnswerHour = botMainSettings.dontAnswerHour
# dontAnswerMinute = botMainSettings.dontAnswerMinute


async def sendNotification(bot: Bot, idTelegram: uuid.UUID, text: str):
    try:
        if idTelegram != "test1":
            await bot.send_message(chat_id=idTelegram, text=text)
    except (TelegramNotFound, TelegramBadRequest) as err:
        print("Error! ", err)
        pass


async def sendDocument(bot: Bot, idTelegram: uuid.UUID, document: InputFile):
    try:
        if idTelegram != "test1":
            await bot.send_message(chat_id=idTelegram, text="Лови бэкап!")
            await bot.send_document(chat_id=idTelegram, document=document)
    except (TelegramNotFound, TelegramBadRequest) as err:
        print("Error! ", err)
        pass


async def getUsersWithActiveMeets(session_pool) -> list:
    # maxDateMeet = await db.getMaxDateMeet()
    async with session_pool() as session:
        maxDateMeet = await getMaxDateMeet(session=session)
        if maxDateMeet:
            now = datetime.now().date()
            # if (now - maxDateMeet).days == (
            #     botMainSettings.commentDayOfWeek - botMainSettings.coreDayOfWeek
            # ):
            # idsTelegram = await db.getLastMeet()
            idsTelegram = await getLastMeet(session=session, maxDateMeet=maxDateMeet)
            return idsTelegram
            # return None
        return None


async def getComments(bot: Bot, session_pool: async_sessionmaker) -> None:
    # if not db.database.is_connected:
    #     await db.database.connect()
    idsTelegram = await getUsersWithActiveMeets(session_pool=session_pool)
    if idsTelegram:
        text = botTextSettings.startShortComment.replace("|", "\n")
        for idTelegram in idsTelegram:
            # await startGetShortComment(bot=bot, idTelegram=idTelegram)
            await sendNotification(bot=bot, idTelegram=idTelegram, text=text)


async def sendNotificationsToAdmins(
    bot: Bot, session_pool: async_sessionmaker, admins: List
) -> None:
    # if not db.database.is_connected:
    #     await db.database.connect()
    async with session_pool() as session:
        df = await getUsersWhichDontAnswer(session=session, use_pandas=True)
    if len(admins) > 0:
        if not df.empty:
            text += botTextSettings.usersDontMeet + "\n"
            for index, row in df.iterrows():
                text += f"{row[1]}\n"
            for admin in admins:
                await sendNotification(bot=bot, idTelegram=admin, text=text)


async def backUp(bot: Bot, admins: List) -> None:
    document = FSInputFile(path=botMainSettings.documentBackUp)
    for admin in admins:
        await sendDocument(bot=bot, idTelegram=admin, document=document)


# async def executeCore(bot, session_pool) -> None:
#     # if not db.database.is_connected:
#     #     await db.database.connect()
#     await generalAlgoritm(
#         bot=bot,
#         session_pool=session_pool,
#     )


# async def executeTest(bot, session_pool) -> None:
#     # if not db.database.is_connected:
#     #     await db.database.connect()
#     await Test(
#         bot=bot,
#         session_pool=session_pool,
#     )


async def executeNotifications(
    bot: Bot,
    session_pool: async_sessionmaker,
    scheduler: AsyncIOScheduler,
    admins: List,
) -> None:
    scheduler.add_job(
        generalAlgoritm,
        "cron",
        day_of_week=botMainSettings.coreDayOfWeek,
        hour=botMainSettings.coreHour,
        minute=botMainSettings.coreMinute,
        id="executeCore",
        args=(bot, session_pool),
    )

    # short comments
    scheduler.add_job(
        getComments,
        "cron",
        day_of_week=botMainSettings.commentDayOfWeek,
        hour=botMainSettings.commentHour,
        minute=botMainSettings.commentMinute,
        id="AskAboutMeet",
        args=(bot, session_pool),
    )

    scheduler.add_job(
        sendNotificationsToAdmins,
        "cron",
        day_of_week=botMainSettings.dontAnswerDayOfWeek,
        hour=botMainSettings.dontAnswerHour,
        minute=botMainSettings.dontAnswerMinute,
        id="Send to admins",
        args=(bot, session_pool, admins),
    )

    # Отправка бэкапа
    scheduler.add_job(
        backUp,
        "cron",
        hour=botMainSettings.backupHour,
        minute=botMainSettings.backupMinute,
        id="BackUps",
        args=(bot, admins),
    )

    scheduler.start()
