import uuid
import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound


from utils.buttons import (
    createMainMenu,
    createBinaryAnswer,
    getListBinaryAnswer,
)
from utils.bd import DataBase
from settings.config import botMainSettings

waitGetComment = botMainSettings.waitGetComment

db = DataBase()

# set way of change registration
class getComments(StatesGroup):
    isFindPartner = State()
    findPartner = State()
    isLike = State()
    whyNotLike = State()


async def startGetComments(bot, idTelegram: str, dp) -> None:
    @dp.async_task
    async def start(bot, idTelegram: str, dp):
        dp.set_current(dp)
        state = dp.current_state(chat=idTelegram, user=idTelegram)
        
        try:
            await bot.send_message(
                idTelegram,
                "Привет! Получилось встретится с партнером?",
                reply_markup=createBinaryAnswer(),
            )
        except ChatNotFound:
            pass
        await state.set_state(getComments.isFindPartner)
        await asyncio.sleep(waitGetComment)
        try:
            data = await state.get_data()
            if data["isFindPartnerNotExceed"] is True:
                pass
        # Если пользователь не ответил или за это время state завершился, получаем KeyError и Сохраняем результат, что он встретился
        except KeyError:
            idUser = await db.getUserRegistrationId(idTelegram=idTelegram)
            idMeet = await db.getIdMeetLastMeet(idUser=idUser)
            if idMeet:
                if not await db.commentExist(idUser=idUser, idMeet=idMeet):
                    currentData = {}
                    currentData["isFindPartner"] = True
                    currentData["isLike"] = True
                    currentData["createBySystem"] = True
                    try:
                        await bot.send_message(
                            idTelegram,
                            f"Жаль, что ты не ответил. Поэтому мы считаем, что встреча состоялась."
                        )
                    except ChatNotFound:
                        pass
                    await insertCommentData(currentData=currentData, idTelegram=idTelegram)
                    await state.finish()
    
    await start(bot=bot, idTelegram=idTelegram, dp=dp)


async def cmdIsFindPartner(message: types.Message, state: FSMContext) -> None:
    await state.update_data(isFindPartnerNotExceed=True)
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(isFindPartner=True if message.text == "Да" else False)
    positiveAnswer = getListBinaryAnswer()[0]
    negativeAnswer = getListBinaryAnswer()[1]
    if message.text == negativeAnswer:
        # await message.answer(
        #     "Найти нового партнера?",
        #     reply_markup=createBinaryAnswer(),
        # )
        # await getComments.findPartner.set()
        # insert data
        currentData = await state.get_data()
        await insertCommentData(currentData=currentData, idTelegram=message.from_user.id)


        messageText = "Нам очень жаль! Надеемся на следующей неделе ты встретишься с новым партнером! До встречи!"
        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            messageText,
            reply_markup=menu,
        )
        await state.finish()

    if message.text == positiveAnswer:
        await message.answer(
            "Все понравилось?",
            reply_markup=createBinaryAnswer(),
        )
        await getComments.isLike.set()


async def cmdFindPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(findPartner=True if message.text == "Да" else False)
    positiveAnswer = getListBinaryAnswer()[0]
    negativeAnswer = getListBinaryAnswer()[1]
    if message.text == positiveAnswer:
        messageText = "Завтра мы тебе сообщим результаты поиска!"

    if message.text == negativeAnswer:
        messageText = "Тогда до следующей недели!"

    # insert data
    currentData = await state.get_data()
    await insertCommentData(currentData=currentData, idTelegram=message.from_user.id)

    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
        messageText,
        reply_markup=menu,
    )
    await state.finish()


async def cmdIsLike(message: types.Message, state: FSMContext) -> None:

    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(isLike=True if message.text == "Да" else False)
    positiveAnswer = getListBinaryAnswer()[0]
    negativeAnswer = getListBinaryAnswer()[1]

    if message.text == positiveAnswer:
        # insert data
        currentData = await state.get_data()
        await insertCommentData(currentData=currentData, idTelegram=message.from_user.id)

        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            "Выберите, действие из меню.",
            reply_markup=menu,
        )
        await state.finish()

    if message.text == negativeAnswer:
        await message.answer(
            "Напиши, почему не понравилось",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await getComments.next()


async def cmdWhyNotLike(message: types.Message, state: FSMContext) -> None:
    answer = message.text
    if len(answer) > 255:
        answer = answer[:255]

    await state.update_data(why=answer)
    currentData = await state.get_data()
    await insertCommentData(currentData=currentData, idTelegram=message.from_user.id)

    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
        "Выберите, действие из меню.",
        reply_markup=menu,
    )
    await state.finish()


async def prepareData(currentData: dict, idTelegram: str) -> dict:

    idUser = await db.getUserRegistrationId(idTelegram=idTelegram)
    idMeet = await db.getIdMeetLastMeet(idUser=idUser)

    return {
        "id": uuid.uuid1(),
        "id_registration": idUser,
        "id_meet": idMeet,
        "is_find_partner": currentData["isFindPartner"],
        "find_partner": currentData.get("findPartner", None),
        "is_like": currentData.get("isLike", None),
        "why": currentData.get("why", None),
        "create_by_system": currentData.get("create_by_system", False),
    }


async def insertCommentData(currentData: dict, idTelegram: str) -> None:
    data = await prepareData(currentData=currentData, idTelegram=idTelegram)

    await db.insertComment(data=data)


def registerHandlersGetComments(dp: Dispatcher) -> None:
    # dp.message_handler(startGetComments, state='*')
    dp.register_message_handler(cmdIsFindPartner, state=getComments.isFindPartner)
    dp.register_message_handler(cmdFindPartner, state=getComments.findPartner)
    dp.register_message_handler(cmdIsLike, state=getComments.isLike)
    dp.register_message_handler(cmdWhyNotLike, state=getComments.whyNotLike)
