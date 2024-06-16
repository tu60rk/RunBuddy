import uuid

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from utils.buttons import (
    createMainMenu,
    chooseGender,
    chooseCity,
    chooseRunLevel,
    createBinaryAnswer,
    getListCities,
    getListRunLevel,
    getListBinaryAnswer,
    getListGender,
    skipInput,
    skipData
)
from utils.bd import DataBase


db = DataBase()

# set way of registration
class Registration(StatesGroup):
    inputName = State()
    inputAge = State()
    chooseSex = State()
    chooseCity = State()
    inputCity = State()
    chooseRunLevel = State()
    inputAccountLink = State()
    chooseRunLevelPartner = State()
    chooseGenderPartner = State()
    chooseOldPartner = State()


async def startRegistration(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer(
        "Напиши имя и фамилию в формате: Иван Иванов",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await Registration.inputName.set()


async def cmdInputName(message: types.Message, state: FSMContext) -> None:
    splitName = message.text.split(" ")
    if len(splitName) != 2 or not splitName[0].isalpha() or not splitName[1].isalpha():
        await message.answer(
            "Что-то не так! Пожалуйста, введи имя без цифр и символов 🙏"
        )
        return

    await state.update_data(name=splitName[0])
    await state.update_data(lastName=splitName[1])
    await message.answer(
        "Напиши возраст",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await Registration.next()


async def cmdInputAge(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Напиши возраст, используя только цифры 🙏")
        return

    if int(message.text) > 100:
        await message.answer(
            "Упс! Тебе правда больше 100 лет? Пожалуйста, введи корректный возраст 🙏"
        )
        return

    if int(message.text) < 18:
        await message.answer(
            "Упс! Тебе правда меньше 18 лет? Извини, но пока что бот доступен с 18 лет 🙏"
        )
        await state.finish()
        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            "Выберите действия из меню ниже",
            reply_markup=menu,
        )

    await state.update_data(age=int(message.text))
    await message.answer(
        "Выбери пол 👫",
        reply_markup=chooseGender(),
    )
    await Registration.next()


async def cmdChooseSex(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListGender():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=chooseGender(),
        )
        return

    await state.update_data(sex=message.text)
    await message.answer(
        "Укажи город 🏙",
        reply_markup=chooseCity(),
    )
    await Registration.next()


async def cmdChooseCity(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListCities():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=chooseCity(),
        )
        return

    if message.text != "Другой":
        await state.update_data(city=message.text)
        await message.answer(
            "Укажи уровень подготовки 💪",
            reply_markup=chooseRunLevel(),
        )
        await Registration.chooseRunLevel.set()
    else:
        await message.answer(
            "Введи свой город 🏙",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await Registration.next()


async def cmdInputCity(message: types.Message, state: FSMContext) -> None:
    splitCity = message.text.split(" ")
    for partCity in splitCity:
        if not partCity.isalpha():
            await message.answer(
                "Неправильно набран город... Пожалуйста, введи название без цифр и символов 🙏"
            )
            return

    await state.update_data(city=message.text)
    await message.answer(
        "Укажи уровень подготовки 💪",
        reply_markup=chooseRunLevel(),
    )
    await Registration.next()


async def cmdChooseRunLevel(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListRunLevel():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=chooseRunLevel(),
        )
        return

    await state.update_data(runLevel=message.text)
    await message.answer(
        "Пришли ссылку на свой аккаунт в любой соцсети",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await Registration.next()


async def cmdInputAccountLink(message: types.Message, state: FSMContext) -> None:
    if message.text == skipData()[0]:
        await state.update_data(accountLink="")
    else:
        await state.update_data(accountLink=message.text)
    await message.answer(
        """Отлично! мы почти завершили регистрацию, осталось пару вопросов

Тебе важен уровень подготовки напарника?""",
        reply_markup=createBinaryAnswer(),
    )
    await Registration.next()


async def cmdChooseRunLevelPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(
        chooseRunLevelPartner=True if message.text == "Да" else False
    )
    await message.answer(
        """Хочешь бегать с людьми противоположного пола?""",
        reply_markup=createBinaryAnswer(),
    )
    await Registration.next()


async def cmdChooseGenderPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(chooseGenderPartner=True if message.text == "Да" else False)
    await message.answer(
        """хочешь бегать со cтарыми партнерами, если алгоритм не подобрал новых?""",
        reply_markup=createBinaryAnswer(),
    )
    await Registration.next()


async def cmdChooseOldPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(chooseOldPartner=True if message.text == "Да" else False)
    currectData = await state.get_data()
    userId = message.from_user.id
    userLinkTelegramAccount = message.from_user.url
    await db.addRegistrationData(
        data=prepareData(currectData, userId, userLinkTelegramAccount)
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
        """На этом все!
Жди понедельник и мы пришлем ссылку на твоего партнера по бегу 🏃🏃‍♀️

До встречи!""",
        reply_markup=menu,
    )
    await state.finish()


def prepareData(currectData, userId, userLinkTelegramAccount) -> dict:
    return {
        "id": uuid.uuid1(),
        "name": currectData["name"],
        "last_name": currectData["lastName"],
        "age": currectData["age"],
        "sex": currectData["sex"],
        "city": currectData["city"],
        "run_level": currectData["runLevel"],
        "account_link": currectData["accountLink"],
        "level_partner_need": currectData["chooseRunLevelPartner"],
        "any_gender": currectData["chooseGenderPartner"],
        "use_old_partner": currectData["chooseOldPartner"],
        "meet_active": True,
        "id_telegram": userId,
        "link_telegram": userLinkTelegramAccount,
    }


def registerHandlersRegistration(dp: Dispatcher) -> None:

    dp.register_message_handler(
        startRegistration,
        Text(equals=["Учавствовать во встречах"], ignore_case=True),
        state="*",
    )
    dp.register_message_handler(cmdInputName, state=Registration.inputName)
    dp.register_message_handler(cmdInputAge, state=Registration.inputAge)
    dp.register_message_handler(cmdChooseSex, state=Registration.chooseSex)
    dp.register_message_handler(cmdChooseCity, state=Registration.chooseCity)
    dp.register_message_handler(cmdInputCity, state=Registration.inputCity)
    dp.register_message_handler(cmdChooseRunLevel, state=Registration.chooseRunLevel)
    dp.register_message_handler(
        cmdInputAccountLink, state=Registration.inputAccountLink
    )
    dp.register_message_handler(
        cmdChooseRunLevelPartner, state=Registration.chooseRunLevelPartner
    )
    dp.register_message_handler(
        cmdChooseGenderPartner, state=Registration.chooseGenderPartner
    )
    dp.register_message_handler(
        cmdChooseOldPartner, state=Registration.chooseOldPartner
    )
