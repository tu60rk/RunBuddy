from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext

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


def registerHandlersCommon(dp: Dispatcher) -> None:
    dp.register_message_handler(startCommandHandler, commands="start", state="*")
