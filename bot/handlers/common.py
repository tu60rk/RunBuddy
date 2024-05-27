from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext

from utils.buttons import create_main_menu
from utils.bd import DataBase

db = DataBase()

# echo handler function
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    is_admin = await db.is_admin(user_id=message.from_user.id)
    is_registration = await db.is_registration(user_id=message.from_user.id)
    await message.reply(
        """Привет!👋
Это команда Run Buddy — бота для нетворкинга на бегу. Мы поможем найти с кем тебе побегать, познакомим с новыми людьми, а новичкам поможем влиться в беговую тусовку!

Каждый понедельник бот будет присылать случайного человека для пробежки — вам останется только связаться друг с другом и договориться об удобной дате.

Но сначала нужно зарегистрироваться, чтобы мы узнали тебя получше и смогли подобрать пару для пробежки. Нажимай на кнопку и начнём!""",
        reply_markup=create_main_menu(
            is_admin=is_admin, is_registration=is_registration
        ),
    )


def register_handlers_common(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command_handler, commands="start", state="*")
