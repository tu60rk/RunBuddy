import os
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from aiogram.contrib.fsm_storage.base import StorageKey
# from aiogram.dispatcher import FSMContext


from utils.core import generalAlgoritm
from handlers.getComments import startGetComments



coreDayOfWeek = int(os.getenv("coreDayOfWeek", 0))
coreHour = int(os.getenv("coreHour", 12))
coreMinute = int(os.getenv("coreMinute", 0))


commentDayOfWeek = int(os.getenv("commentDayOfWeek", 2))
commentHour = int(os.getenv("commentHour", 12))
commentMinute = int(os.getenv("commentMinute", 0))


doubleCoreDayOfWeek = int(os.getenv("doubleCoreDayOfWeek", 3))
doubleCoreHour = int(os.getenv("doubleCoreHour", 12))
doubleCoreMinute = int(os.getenv("doubleCoreMinute", 2))


async def getUsersWithActiveMeets(db) -> list:
    # maxDateMeet = datetime.strptime(await db.getMaxDateMeet(), "%Y.%m.%d %H:%M:%S")
    maxDateMeet = await db.getMaxDateMeet()
    now = datetime.now().date()
    print('maxDateMeet: ', maxDateMeet)
    print('nowWeekday: ', now)
    if (now - maxDateMeet).days == (commentDayOfWeek - coreDayOfWeek):
        idsTelegram = await db.getLastMeet()
        return idsTelegram
    return None
# psql -h 127.0.0.1 -U run -d run_database;
# postgres://run:RunBuddyPassword@db:5432/run_database
# до конца проверить работу комментариев:
    # - вставить фековую встречу
    # - вставить фекового юзера
    # - 
    # - 


# максимальная дата алгоритма и текущая дата

async def getComments(bot, db, dp) -> None:
    if not db.database.is_connected:
        await db.database.connect()

    idsTelegram = await getUsersWithActiveMeets(db=db)
    if idsTelegram:
        for idTelegram in idsTelegram:
            # print('Telegram id: ', idTelegram)
            # if idTelegram == 'test1':
            #     continue
            # сформируем состояние
            # stateKey = StorageKey(bot.id, idTelegram, idTelegram)
            # state = FSMContext(storage=storage, chat=idTelegram, user=idTelegram)
            await startGetComments(bot=bot, idTelegram=idTelegram, dp=dp)


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
    scheduler.add_job(
        getComments,
        "cron",
        day_of_week=commentDayOfWeek,
        hour=commentHour,
        minute=commentMinute,
        id="getComments",
        args=(bot, db, dp),
    )
    scheduler.start()
