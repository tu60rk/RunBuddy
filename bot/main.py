import asyncio

# from datetime import datetime
# import threading
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

# from aiogram.utils.executor import start_webhook
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from handlers import (
    common,
    adminPanel,
    registration,
    changeDataRegistration,
    shortComment,
)
from middlewares import DbSessionMiddleware, MenuMiddleware


# from handlers.registration import registerHandlersRegistration
# from handlers.changeDataRegistration import registerHandlersChangeDataRegistration
# from handlers.getComments import registerHandlersGetComments
# from handlers.shortComment import registerHandlersGetShortComments
# from handlers.adminPanel import registerHandlersAdmin
# from utils.bd import DataBase
from utils.notifications import executeNotifications
from settings.config import botMainSettings, botMainDbSettings, botTextSettings


logger = logging.getLogger(__name__)


# webhook settings
# WEBHOOK_HOST = f"https://{botMainSettings.NGINX_HOST}"
# WEBHOOK_PATH = "/webhook"
# WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# bot initialization
# bot = Bot(token=botMainSettings.TELEGRAM_TOKEN)
# loop = asyncio.get_event_loop()
# dp = Dispatcher(bot, storage=MemoryStorage())
# dp = Dispatcher(storage=MemoryStorage())

# var_1 = bot
# dp['var_1'] = bot

# registerHandlersCommon(dp)
# registerHandlersRegistration(dp)
# registerHandlersChangeDataRegistration(dp)
# registerHandlersGetComments(dp)
# registerHandlersGetShortComments(dp)
# registerHandlersAdmin(dp)


# db = DataBase()


# def between_callback(loop) -> None:
#     asyncio.set_event_loop(loop)
#     loop.create_task(executeNotifications(bot=bot, db=db, dp=dp))


# def executeTread():
#     loop = asyncio.get_event_loop()
#     thread = threading.Thread(target=between_callback, args=(loop,), daemon=True)
#     thread.start()


# webhook startup & shutdown
# async def webhookOnStartup(dp, var_1) -> None:
#     # executeTread()

#     if not db.database.is_connected:
#         await db.database.connect()
#     await var_1.set_webhook(WEBHOOK_URL)


# async def webhookOnShutdown(dp, var_1):
#     if db.database.is_connected:
#         await db.database.disconnect()
#     await var_1.delete_webhook()


# pooling startup & shutdown
# async def poolingOnStartup(dp) -> None:
#     # executeTread()

#     if not db.database.is_connected:
# await db.database.connect()


# async def poolingOnShutdown(dp, var_1):
#     if db.database.is_connected:
#         await db.database.disconnect()
#     await var_1.close()


async def main():

    # connection to db
    engine = create_async_engine(
        url=str(botMainDbSettings.dsl_database),  # здесь требуется приведение к строке
        echo=True,
    )

    # Проверка соединения с СУБД
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    admins = [int(i) for i in botMainSettings.ADMINS.split(",")]
    bot = Bot(token=botMainSettings.TELEGRAM_TOKEN)
    dp = Dispatcher(
        admins=admins,
        bot=bot,
        storage=MemoryStorage(),
        db_engine=engine,
        botMainSettings=botMainSettings,
        botMainDbSettings=botMainDbSettings,
        botTextSettings=botTextSettings,
    )

    # Подключение middleware
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.update.outer_middleware(MenuMiddleware())

    # Подготовим планировщики
    scheduler = AsyncIOScheduler()
    await executeNotifications(
        bot=bot, session_pool=Sessionmaker, scheduler=scheduler, admins=admins
    )

    # Регистриуем роутеры в диспетчере
    dp.include_router(common.router)
    dp.include_router(registration.router)
    dp.include_router(adminPanel.router)
    dp.include_router(changeDataRegistration.router)
    dp.include_router(shortComment.router)

    if not botMainSettings.IS_WEBHOOK:
        await dp.start_polling(
            bot,
            skip_updates=True,
            # on_startup=poolingOnStartup,
            # on_shutdown=poolingOnShutdown,
        )
    else:
        WEBHOOK_HOST = f"https://{botMainSettings.NGINX_HOST}"
        WEBHOOK_PATH = "/webhook"
        WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types(),
        )

        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(
            runner, host=botMainSettings.WEBAPP_HOST, port=botMainSettings.WEBAPP_PORT
        )
        await site.start()
        await asyncio.Event().wait()


# bot startup
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

    # dp.run_polling(bot)
    # asyncio.run(main())

    # dp.start_polling(
    #     bot,
    #     skip_updates=True,
    #     on_startup=poolingOnStartup,
    #     on_shutdown=poolingOnShutdown,
    # )

    # if botMainSettings.IS_WEBHOOK == True:
    #     print(datetime.now())
    #     start_webhook(
    #         dispatcher=dp,
    #         webhook_path=WEBHOOK_PATH,
    #         on_startup=webhookOnStartup,
    #         on_shutdown=webhookOnShutdown,
    #         skip_updates=True,
    #         host=botMainSettings.WEBAPP_HOST,
    #         port=botMainSettings.WEBAPP_PORT,

    #     )
    # else:
    # dp.start_polling(
    #     bot,
    #     skip_updates=True,
    #     on_startup=poolingOnStartup,
    #     on_shutdown=poolingOnShutdown,
    # )
