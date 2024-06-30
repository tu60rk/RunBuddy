import os
import asyncio
import asyncpg
import threading
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.common import registerHandlersCommon
from handlers.registration import registerHandlersRegistration
from handlers.changeDataRegistration import registerHandlersChangeDataRegistration
from handlers.getComments import registerHandlersGetComments
from utils.bd import DataBase
from utils.notifications import executeNotifications

# global variable to switch between polling|webhook for debug/local start
# IS_WEBHOOK = 1
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
NGINX_HOST = os.environ.get("NGINX_HOST")
IS_WEBHOOK = os.environ.get("IS_WEBHOOK")

# webhook settings
WEBHOOK_HOST = f"https://{NGINX_HOST}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.environ.get("WEBAPP_HOST")
WEBAPP_PORT = int(os.environ.get("WEBAPP_PORT"))

# bot initialization
bot = Bot(token=TELEGRAM_TOKEN)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

registerHandlersCommon(dp)
registerHandlersRegistration(dp)
registerHandlersChangeDataRegistration(dp)
registerHandlersGetComments(dp)


db = DataBase()


def between_callback(loop) -> None:
    asyncio.set_event_loop(loop)
    loop.create_task(executeNotifications(bot=bot, db=db, dp=dp))


# webhook startup & shutdown
async def webhookOnStartup(dp) -> None:
    if not db.database.is_connected:
        await db.database.connect()
    await bot.set_webhook(WEBHOOK_URL)


async def webhookOnShutdown(dp):
    if db.database.is_connected:
        await db.database.disconnect()
    await bot.delete_webhook()


# pooling startup & shutdown
async def poolingOnStartup(dp) -> None:
    if not db.database.is_connected:
        await db.database.connect()


async def poolingOnShutdown(dp):
    if db.database.is_connected:
        await db.database.disconnect()
    await bot.close()


# bot startup
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=between_callback, args=(loop,), daemon=True)
    thread.start()

    if IS_WEBHOOK == 1:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=webhookOnStartup,
            on_shutdown=webhookOnShutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=poolingOnStartup,
            on_shutdown=poolingOnShutdown,
        )
