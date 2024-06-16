from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from utils.buttons import (
    createMainMenu,
    chooseCity,
    chooseRunLevel,
    createBinaryAnswer,
    getListCities,
    getListRunLevel,
    getListBinaryAnswer,
    registrationUpdateData,
    getListColumnUpdateRegistration,
)
from utils.bd import DataBase


db = DataBase()

# set way of change registration
class changeRegistration(StatesGroup):
    choose = State()
    chooseCity = State()
    inputCity = State()
    chooseRunLevel = State()
    inputAccountLink = State()
    chooseRunLevelPartner = State()
    chooseGenderPartner = State()
    changeMeetStatus = State()


async def startChangeRegistration(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer(
        "Какие данные вы хотите изменить?",
        reply_markup=registrationUpdateData(),
    )
    await changeRegistration.choose.set()


async def cmdChoose(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListColumnUpdateRegistration():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=registrationUpdateData(),
        )
        return

    if message.text == getListColumnUpdateRegistration()[0]:
        await message.answer(
            "Укажи город 🏙",
            reply_markup=chooseCity(),
        )
        await changeRegistration.chooseCity.set()

    if message.text == getListColumnUpdateRegistration()[1]:
        await message.answer(
            "Укажи уровень подготовки 💪",
            reply_markup=chooseRunLevel(),
        )
        await changeRegistration.chooseRunLevel.set()

    if message.text == getListColumnUpdateRegistration()[2]:
        await message.answer(
            """Тебе важен уровень подготовки напарника?""",
            reply_markup=createBinaryAnswer(),
        )
        await changeRegistration.chooseRunLevelPartner.set()

    if message.text == getListColumnUpdateRegistration()[3]:
        await message.answer(
            "Хочешь учавствовать во встречах?",
            reply_markup=createBinaryAnswer(),
        )
        await changeRegistration.changeMeetStatus.set()

    if message.text == getListColumnUpdateRegistration()[4]:
        await message.answer(
            "Пришли ссылку на свой аккаунт в любой соцсети",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await changeRegistration.inputAccountLink.set()

    if message.text == getListColumnUpdateRegistration()[5]:
        await message.answer(
            """Хочешь бегать с людьми противоположного пола?""",
            reply_markup=createBinaryAnswer(),
        )
        await changeRegistration.chooseGenderPartner.set()
    
    if message.text == getListColumnUpdateRegistration()[6]:
        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer("""Выберите дальнейшие действие""", reply_markup=menu)
        await state.finish()


async def cmdChooseCity(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListCities():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=chooseCity(),
        )
        return

    if message.text != "Другой":
        await db.updateRegistrationData(
            userId=message.from_user.id, columnName="city", data=message.text
        )

        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            """Выберите дальнейшие действие""",
            reply_markup=menu,
        )
        await state.finish()
    else:
        await message.answer(
            "Введи свой город 🏙",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await changeRegistration.inputCity.set()


async def cmdInputCity(message: types.Message, state: FSMContext) -> None:
    splitCity = message.text.split(" ")
    for partCity in splitCity:
        if not partCity.isalpha():
            await message.answer(
                "Неправильно набран город... Пожалуйста, введи название без цифр и символов 🙏"
            )
            return

    await db.updateRegistrationData(
        userId=message.from_user.id, columnName="city", data=message.text
    )

    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer("""Выберите дальнейшие действие""", reply_markup=menu)
    await state.finish()


async def cmdChooseRunLevel(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListRunLevel():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=chooseRunLevel(),
        )
        return

    await db.updateRegistrationData(
        userId=message.from_user.id, columnName="run_level", data=message.text
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer("""Выберите дальнейшие действие""", reply_markup=menu)
    await state.finish()


async def cmdInputAccountLink(message: types.Message, state: FSMContext) -> None:
    await db.updateRegistrationData(
        userId=message.from_user.id, columnName="account_link", data=message.text
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer("""Выберите дальнейшие действие""", reply_markup=menu)
    await state.finish()


async def cmdChooseRunLevelPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return
    await db.updateRegistrationData(
        userId=message.from_user.id,
        columnName="level_partner_need",
        data=True if message.text == "Да" else False,
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer("""Выберите дальнейшие действие""", reply_markup=menu)
    await state.finish()


async def cmdChooseGenderPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return
    await db.updateRegistrationData(
        userId=message.from_user.id,
        columnName="any_gender",
        data=True if message.text == "Да" else False,
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer("""Выберите дальнейшие действие""", reply_markup=menu)
    await state.finish()


async def cmdChangeMeetStatus(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            "Пожалуйста, выберите из пунктов ниже.",
            reply_markup=createBinaryAnswer(),
        )
        return
    await db.updateRegistrationData(
        userId=message.from_user.id,
        columnName="meet_active",
        data=True if message.text == "Да" else False,
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer("""Выберите дальнейшие действие""", reply_markup=menu)
    await state.finish()


def registerHandlersChangeDataRegistration(dp: Dispatcher) -> None:

    dp.register_message_handler(
        startChangeRegistration,
        Text(equals=["Изменить данные"], ignore_case=True),
        state="*",
    )
    dp.register_message_handler(cmdChoose, state=changeRegistration.choose)
    dp.register_message_handler(cmdChooseCity, state=changeRegistration.chooseCity)
    dp.register_message_handler(cmdInputCity, state=changeRegistration.inputCity)
    dp.register_message_handler(
        cmdChooseRunLevel, state=changeRegistration.chooseRunLevel
    )
    dp.register_message_handler(
        cmdInputAccountLink, state=changeRegistration.inputAccountLink
    )
    dp.register_message_handler(
        cmdChooseRunLevelPartner, state=changeRegistration.chooseRunLevelPartner
    )
    dp.register_message_handler(
        cmdChooseGenderPartner, state=changeRegistration.chooseGenderPartner
    )
    dp.register_message_handler(
        cmdChangeMeetStatus, state=changeRegistration.changeMeetStatus
    )
