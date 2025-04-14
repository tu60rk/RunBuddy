from aiogram import types, Router, F, Bot

# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.filters import MagicData, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

# from aiogram.utils.formatting import Text
from aiogram.types.input_file import FSInputFile
from aiogram.types import ReplyKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from db.request import getRegisteredUsers, getMeetsQ, getCommentsQ, getUsers, setActive

# from utils.buttons import createMainMenu

# from utils.bd import DataBase
from settings.config import botTextSettings, botMainSettings

# db = DataBase()
botAdminText = botTextSettings.menuForAdmins.split("|")
# bot = Bot(token=botMainSettings.TELEGRAM_TOKEN)

router = Router(name="admin commands router")
router.message.filter(MagicData(F.event.chat.id.in_(F.admins)))


class admin(StatesGroup):
    sendMessage = State()


@router.message(F.text == botAdminText[0], StateFilter(default_state))
async def getRegisteredPeoople(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    menu: ReplyKeyboardMarkup,
) -> None:
    # await state.finish()
    # menu = await createMainMenu(
    #     userId=message.from_user.id, session=session, admins=admins
    # )
    # if db.isAdmin(userId=message.from_user.id):
    # df = await db.getRegisteredUsers()
    df = await getRegisteredUsers(session=session, use_pandas=True)
    pathFile = botMainSettings.path + botMainSettings.fileNameRegistered
    df.to_excel(pathFile)
    # text_file = InputFile(pathFile, filename=botMainSettings.fileNameRegistered)
    text_file = FSInputFile(pathFile, filename=botMainSettings.fileNameRegistered)

    await message.answer_document(
        text_file,
        reply_markup=menu,
    )
    # else:
    #     await message.answer(
    #         botTextSettings.menuException,
    #         reply_markup=menu,
    #     )
    # await state.finish()
    await state.clear()


@router.message(F.text == botAdminText[1], StateFilter(default_state))
async def getMeets(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    menu: ReplyKeyboardMarkup,
) -> None:
    # await state.finish()
    # menu = await createMainMenu(
    #     userId=message.from_user.id, session=session, admins=admins
    # )
    # if db.isAdmin(userId=message.from_user.id):
    # df = await db.getMeets()
    df = await getMeetsQ(session=session, use_pandas=True)
    pathFile = botMainSettings.path + botMainSettings.fileNameMeets
    df.to_excel(pathFile)
    # text_file = InputFile(pathFile, filename=botMainSettings.fileNameMeets)
    text_file = FSInputFile(pathFile, filename=botMainSettings.fileNameMeets)
    await message.answer_document(
        text_file,
        reply_markup=menu,
    )
    # else:
    #     await message.answer(
    #         botTextSettings.menuException,
    #         reply_markup=menu,
    #     )
    # await state.finish()
    await state.clear()


@router.message(F.text == botAdminText[2], StateFilter(default_state))
async def getComments(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    menu: ReplyKeyboardMarkup,
) -> None:
    # await state.finish()
    # isCanGetComment = await db.isCanGetComment(userId=message.from_user.id)
    # menu = await createMainMenu(
    #     userId=message.from_user.id, session=session, admins=admins
    # )
    # if db.isAdmin(userId=message.from_user.id):
    # df = await db.getComments()
    df = await getCommentsQ(session=session, use_pandas=True)
    pathFile = botMainSettings.path + botMainSettings.fileNameComments
    df.to_excel(pathFile)
    # text_file = InputFile(pathFile, filename=botMainSettings.fileNameComments)
    text_file = FSInputFile(pathFile, filename=botMainSettings.fileNameComments)
    await message.answer_document(
        text_file,
        reply_markup=menu,
    )
    # else:
    #     await message.answer(
    #         botTextSettings.menuException,
    #         reply_markup=menu,
    #     )
    # await state.finish()
    await state.clear()


@router.message(F.text == botAdminText[3], StateFilter(default_state))
async def preSendMessage(message: types.Message, state: FSMContext) -> None:
    # await state.finish()
    # if db.isAdmin(userId=message.from_user.id):
    await message.answer(
        "Введи любой текст, который хочешь отправить активным пользователям.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(admin.sendMessage)
    # await admin.sendMessage.set()

    # else:
    #     menu = await createMainMenu(userId=message.from_user.id)
    #     await message.answer(
    #         botTextSettings.menuException,
    #         reply_markup=menu,
    #     )


@router.message(StateFilter(admin.sendMessage))
async def cmdSendMessage(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    bot: Bot,
    menu: ReplyKeyboardMarkup,
) -> None:
    if not message.text:
        await message.answer(
            "Ты ничего не ввел! Давай попробуем снова.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        return

    # users = await db.getUsers()
    users = await getUsers(session=session)
    for row in users:
        user_id = row[0]
        active = row[1]
        try:
            # await bot.send_message(user_id, message.text)
            await bot.send_message(user_id, message.text)
            if active != True:
                # await db.setActive(user_id, True)
                await setActive(session, user_id, True)
        except:
            # await db.setActive(user_id, False)
            await setActive(session, user_id, False)

    # menu = await createMainMenu(
    #     userId=message.from_user.id, session=session, admins=admins
    # )
    await bot.send_message(
        message.from_user.id,
        "Успешно отправлено!",
        reply_markup=menu,
    )
    # await state.finish()
    await state.clear()


# def registerHandlersAdmin(dp: Dispatcher) -> None:
#     dp.register_message_handler(
#         getRegisteredPeoople,
#         Text(equals=[botAdminText[0]], ignore_case=True),
#         state="*",
#     )
#     dp.register_message_handler(
#         getMeets,
#         Text(equals=[botAdminText[1]], ignore_case=True),
#         state="*",
#     )
#     dp.register_message_handler(
#         getComments,
#         Text(equals=[botAdminText[2]], ignore_case=True),
#         state="*",
#     )
#     dp.register_message_handler(
#         preSendMessage,
#         Text(equals=[botAdminText[3]], ignore_case=True),
#         state="*",
#     )
#     dp.register_message_handler(cmdSendMessage, state=admin.sendMessage)
