from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from aiogram.contrib.fsm_storage.base import StorageKey
# from aiogram.dispatcher import FSMContext


from utils.core import generalAlgoritm
from handlers.getComments import startGetComments
from handlers.shortComment import startGetShortComment
from settings.config import botMainSettings



coreDayOfWeek = botMainSettings.coreDayOfWeek
coreHour = botMainSettings.coreHour
coreMinute = botMainSettings.coreMinute

activateComments = botMainSettings.activateComments
commentDayOfWeek = botMainSettings.commentDayOfWeek
commentHour = botMainSettings.commentHour
commentMinute = botMainSettings.commentMinute




async def getUsersWithActiveMeets(db) -> list:
    maxDateMeet = await db.getMaxDateMeet()
    now = datetime.now().date()
    if (now - maxDateMeet).days == (commentDayOfWeek - coreDayOfWeek):
        idsTelegram = await db.getLastMeet()
        return idsTelegram
    return None


async def getComments(bot, db, dp, isShort: bool) -> None:
    if not db.database.is_connected:
        await db.database.connect()

    idsTelegram = await getUsersWithActiveMeets(db=db)
    if idsTelegram:
        for idTelegram in idsTelegram:
            if not isShort:
                await startGetComments(bot=bot, idTelegram=idTelegram, dp=dp)
            else:
                await startGetShortComment(bot=bot, idTelegram=idTelegram, dp=dp)


async def executeCore(bot, db) -> None:
    if not db.database.is_connected:
        await db.database.connect()
    await generalAlgoritm(
        bot=bot,
        db=db,
    )

async def executeNotifications(bot, db, dp) -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        executeCore,
        "cron",
        day_of_week=coreDayOfWeek,
        hour=coreHour,
        minute=coreMinute,
        id="executeCore",
        args=(bot, db),
    )

    # short comments
    scheduler.add_job(
        getComments,
        "cron",
        day_of_week=commentDayOfWeek,
        hour=commentHour,
        minute=commentMinute,
        id="getComments",
        args=(bot, db, dp, True),
        )


    # if activateComments:
    #     scheduler.add_job(
    #         getComments,
    #         "cron",
    #         day_of_week=commentDayOfWeek,
    #         hour=commentHour,
    #         minute=commentMinute,
    #         id="getComments",
    #         args=(bot, db, dp),
    #     )
    scheduler.start()
