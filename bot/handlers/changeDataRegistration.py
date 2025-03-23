import asyncio

from aiogram import Dispatcher, types

# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text

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
from settings.config import botTextSettings


db = DataBase()

# common text
menuText = botTextSettings.menuText.replace("|", "\n")
menuSuccess = botTextSettings.menuSuccess.replace("|", "\n")
exceptionText = botTextSettings.exceptionText.replace("|", "\n")

# text for change data
changeDataStart = botTextSettings.changeDataStart.replace("|", "\n")

# registration Data
registrationTextCity = botTextSettings.registrationTextCity.replace("|", "\n")
registrationTextInputCity = botTextSettings.registrationTextInputCity.replace("|", "\n")
registrationTextInputCityException = (
    botTextSettings.registrationTextInputCityException.replace("|", "\n")
)
registrationTextRunLevel = botTextSettings.registrationTextRunLevel.replace("|", "\n")
registrationTextInputLinkAccount = (
    botTextSettings.registrationTextInputLinkAccount.replace("|", "\n")
)
registrationTextAdditionalQuestionOne = (
    botTextSettings.registrationTextAdditionalQuestionOne.replace("|", "\n")
)
registrationTextAdditionalQuestionTwo = (
    botTextSettings.registrationTextAdditionalQuestionTwo.replace("|", "\n")
)
registrationTextAdditionalQuestionThree = (
    botTextSettings.registrationTextAdditionalQuestionThree.replace("|", "\n")
)
registrationTextFinalText = botTextSettings.registrationTextFinalText.replace("|", "\n")
changeDataQuestionAboutMeet = botTextSettings.changeDataQuestionAboutMeet.replace(
    "|", "\n"
)

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
        changeDataStart,
        reply_markup=registrationUpdateData(),
    )
    await changeRegistration.choose.set()


async def cmdChoose(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListColumnUpdateRegistration():
        await message.answer(
            exceptionText,
            reply_markup=registrationUpdateData(),
        )
        return

    if message.text == getListColumnUpdateRegistration()[0]:
        await message.answer(
            registrationTextCity,
            reply_markup=chooseCity(),
        )
        await changeRegistration.chooseCity.set()

    if message.text == getListColumnUpdateRegistration()[1]:
        await message.answer(
            registrationTextRunLevel,
            reply_markup=chooseRunLevel(),
        )
        await changeRegistration.chooseRunLevel.set()

    if message.text == getListColumnUpdateRegistration()[2]:
        await message.answer(
            registrationTextAdditionalQuestionOne,
            reply_markup=createBinaryAnswer(),
        )
        await changeRegistration.chooseRunLevelPartner.set()

    if message.text == getListColumnUpdateRegistration()[3]:
        await message.answer(
            changeDataQuestionAboutMeet,
            reply_markup=createBinaryAnswer(),
        )
        await changeRegistration.changeMeetStatus.set()

    if message.text == getListColumnUpdateRegistration()[4]:
        await message.answer(
            registrationTextInputLinkAccount,
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await changeRegistration.inputAccountLink.set()

    if message.text == getListColumnUpdateRegistration()[5]:
        await message.answer(
            registrationTextAdditionalQuestionTwo,
            reply_markup=createBinaryAnswer(),
        )
        await changeRegistration.chooseGenderPartner.set()

    if message.text == getListColumnUpdateRegistration()[6]:
        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(menuSuccess, reply_markup=menu)
        await state.finish()


async def cmdChooseCity(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListCities():
        await message.answer(
            exceptionText,
            reply_markup=chooseCity(),
        )
        return

    if message.text != "Другой":
        await db.updateRegistrationData(
            userId=message.from_user.id, columnName="city", data=message.text
        )

        menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            menuSuccess,
            reply_markup=menu,
        )
        await state.finish()
    else:
        await message.answer(
            registrationTextInputCity,
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await changeRegistration.inputCity.set()


async def cmdInputCity(message: types.Message, state: FSMContext) -> None:
    splitCity = message.text.split(" ")
    for partCity in splitCity:
        if not partCity.isalpha():
            await message.answer(registrationTextInputCityException)
            return

    await db.updateRegistrationData(
        userId=message.from_user.id, columnName="city", data=message.text
    )

    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(menuSuccess, reply_markup=menu)
    await state.finish()


async def cmdChooseRunLevel(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListRunLevel():
        await message.answer(
            exceptionText,
            reply_markup=chooseRunLevel(),
        )
        return

    await db.updateRegistrationData(
        userId=message.from_user.id, columnName="run_level", data=message.text
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(menuSuccess, reply_markup=menu)
    await state.finish()


async def cmdInputAccountLink(message: types.Message, state: FSMContext) -> None:
    await db.updateRegistrationData(
        userId=message.from_user.id, columnName="account_link", data=message.text
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(menuSuccess, reply_markup=menu)
    await state.finish()


async def cmdChooseRunLevelPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            exceptionText,
            reply_markup=createBinaryAnswer(),
        )
        return
    await db.updateRegistrationData(
        userId=message.from_user.id,
        columnName="level_partner_need",
        data=True if message.text == "Да" else False,
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(menuSuccess, reply_markup=menu)
    await state.finish()


async def cmdChooseGenderPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            exceptionText,
            reply_markup=createBinaryAnswer(),
        )
        return
    await db.updateRegistrationData(
        userId=message.from_user.id,
        columnName="any_gender",
        data=True if message.text == "Да" else False,
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(menuSuccess, reply_markup=menu)
    await state.finish()


async def cmdChangeMeetStatus(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            exceptionText,
            reply_markup=createBinaryAnswer(),
        )
        return
    await db.updateRegistrationData(
        userId=message.from_user.id,
        columnName="meet_active",
        data=True if message.text == "Да" else False,
    )
    menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(menuSuccess, reply_markup=menu)
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
