import uuid

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.buttons import (
    createMainMenu,
    createBinaryAnswer,
    getListBinaryAnswer,
)
from utils.bd import DataBase


db = DataBase()

# set way of change registration
class getComments(StatesGroup):
    isFindPartner = State()
    findPartner = State()
    isLike = State()
    whyNotLike = State()


async def startGetComments(bot, userId:str, state: FSMContext) -> None:
    await state.finish()
    await bot.send_message(userId, "Привет! Получилось встретится с партнером?", reply_markup=createBinaryAnswer())
    await getComments.isFindPartner.set()

async def cmdIsFindPartner(message: types.Message, state: FSMContext) -> None:
    
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
        await message.answer(
            "Найти нового партнера?",
            reply_markup=createBinaryAnswer(),
        )
        await getComments.findPartner.set()
    
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
    currectData = await state.get_data()
    await insertCommentData(currectData=currectData)

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
        currectData = await state.get_data()
        await insertCommentData(currectData=currectData)
        
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
    currectData = await state.get_data()
    await insertCommentData(currectData=currectData)

    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
            "Выберите, действие из меню.",
            reply_markup=menu,
        )
    await state.finish()


async def prepareData(currectData: dict, idTelegram: str) -> dict:
    
    idUser= await db.getUserRegistrationId(idTelegram=idTelegram)
    idMeet = await db.getIdMeetLastMeet(idUser=idUser)

    return {
        "id": uuid.uuid1(),
        "id_registration": idUser,
        "id_meet": idMeet,
        "is_find_partner": currectData["isFindPartner"],
        "find_partner": currectData.get("findPartner", None),
        "is_like": currectData.get("isLike", None),
        "why": currectData.get("why", None),
    }

async def insertCommentData(currectData: dict, idTelegram: str) -> None:
    data = await prepareData(
        currectData=currectData,
        idTelegram=idTelegram
    )

    await db.insertComment(data=data)

def registerHandlersGetComments(dp: Dispatcher) -> None:

    dp.register_message_handler(cmdIsFindPartner, state=getComments.isFindPartner)
    dp.register_message_handler(cmdFindPartner, state=getComments.findPartner)
    dp.register_message_handler(cmdIsLike, state=getComments.isLike)
    dp.register_message_handler(cmdWhyNotLike, state=getComments.whyNotLike)