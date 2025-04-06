import uuid

from aiogram import types, Router, F

# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text

from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from db.request import addRegistrationData
from utils.buttons import (
    # createMainMenu,
    chooseGender,
    chooseCity,
    chooseRunLevel,
    createBinaryAnswer,
    getListCities,
    getListRunLevel,
    getListBinaryAnswer,
    getListGender,
    skipInput,
    skipData,
)

# from utils.bd import DataBase
from settings.config import botTextSettings

router = Router()

# menu text
menuText = botTextSettings.menuText.replace("|", "\n")
exceptionText = botTextSettings.exceptionText.replace("|", "\n")

registrationDontHaveData = botTextSettings.registrationDontHaveData.replace("|", "\n")
registrationTextFIO = botTextSettings.registrationTextFIO.replace("|", "\n")
registrationTextFIOException = botTextSettings.registrationTextFIOException.replace(
    "|", "\n"
)
registrationTextInputAge = botTextSettings.registrationTextInputAge.replace("|", "\n")
registrationTextInputAgeException = (
    botTextSettings.registrationTextInputAgeException.replace("|", "\n")
)
registrationTextInputAgeException100 = (
    botTextSettings.registrationTextInputAgeException100.replace("|", "\n")
)
registrationTextInputAgeException18 = (
    botTextSettings.registrationTextInputAgeException18.replace("|", "\n")
)
registrationTextGender = botTextSettings.registrationTextGender.replace("|", "\n")
registrationTextCity = botTextSettings.registrationTextCity.replace("|", "\n")
registrationTextInputCity = botTextSettings.registrationTextInputCity.replace("|", "\n")
registrationTextInputCityException = (
    botTextSettings.registrationTextInputCityException.replace("|", "\n")
)
registrationTextRunLevel = botTextSettings.registrationTextRunLevel.replace("|", "\n")
registrationTextInputLinkAccount = (
    botTextSettings.registrationTextInputLinkAccount.replace("|", "\n")
)
registrationTextAdditionalPreQuestionText = (
    botTextSettings.registrationTextAdditionalPreQuestionText.replace("|", "\n")
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


# db = DataBase()


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
    # chooseOldPartner = State()


@router.message(F.text == "Учавствовать во встречах", StateFilter(default_state))
async def startRegistration(
    message: types.Message,
    state: FSMContext,
    menu: ReplyKeyboardMarkup,
) -> None:
    # await state.finish()
    try:
        phoneNumber = message.contact.phone_number
    except:
        phoneNumber = ""

    try:
        userName = message.from_user.username
    except:
        userName = ""

    if not userName and not phoneNumber:
        # menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            registrationDontHaveData,
            reply_markup=menu,
        )
        return

    await message.answer(
        registrationTextFIO,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    # await Registration.inputName.set()
    await state.set_state(Registration.inputName)


@router.message(StateFilter(Registration.inputName))
async def cmdInputName(message: types.Message, state: FSMContext) -> None:
    splitName = message.text.split(" ")
    if len(splitName) != 2 or not splitName[0].isalpha() or not splitName[1].isalpha():
        await message.answer(registrationTextFIOException)
        return

    await state.update_data(name=splitName[0])
    await state.update_data(lastName=splitName[1])
    await message.answer(
        registrationTextInputAge,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    # await Registration.next()
    await state.set_state(Registration.inputAge)


@router.message(StateFilter(Registration.inputAge))
async def cmdInputAge(
    message: types.Message,
    state: FSMContext,
    menu: ReplyKeyboardMarkup,
) -> None:
    if not message.text.isdigit():
        await message.answer(registrationTextInputAgeException)
        return

    if int(message.text) > 100:
        await message.answer(registrationTextInputAgeException100)
        return

    if int(message.text) < 18:
        await state.finish()
        # menu = await createMainMenu(userId=message.from_user.id)
        await message.answer(
            registrationTextInputAgeException18,
            reply_markup=menu,
        )

    await state.update_data(age=int(message.text))
    await message.answer(
        registrationTextGender,
        reply_markup=chooseGender(),
    )
    # await Registration.next()
    await state.set_state(Registration.chooseSex)


@router.message(StateFilter(Registration.chooseSex))
async def cmdChooseSex(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListGender():
        await message.answer(
            exceptionText,
            reply_markup=chooseGender(),
        )
        return

    await state.update_data(sex=message.text)
    await message.answer(
        registrationTextCity,
        reply_markup=chooseCity(),
    )
    # await Registration.next()
    await state.set_state(Registration.chooseCity)


@router.message(StateFilter(Registration.chooseCity))
async def cmdChooseCity(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListCities():
        await message.answer(
            exceptionText,
            reply_markup=chooseCity(),
        )
        return

    if message.text != "Другой":
        await state.update_data(city=message.text)
        await message.answer(
            registrationTextRunLevel,
            reply_markup=chooseRunLevel(),
        )
        # await Registration.chooseRunLevel.set()
        await state.set_state(Registration.chooseRunLevel)
    else:
        await message.answer(
            registrationTextInputCity,
            reply_markup=types.ReplyKeyboardRemove(),
        )
        # await Registration.next()
        await state.set_state(Registration.inputCity)


@router.message(StateFilter(Registration.inputCity))
async def cmdInputCity(message: types.Message, state: FSMContext) -> None:
    splitCity = message.text.split(" ")
    for partCity in splitCity:
        if not partCity.isalpha():
            await message.answer(registrationTextInputCityException)
            return

    await state.update_data(city=message.text)
    await message.answer(
        registrationTextRunLevel,
        reply_markup=chooseRunLevel(),
    )
    # await Registration.next()
    await state.set_state(Registration.chooseRunLevel)


@router.message(StateFilter(Registration.chooseRunLevel))
async def cmdChooseRunLevel(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListRunLevel():
        await message.answer(
            exceptionText,
            reply_markup=chooseRunLevel(),
        )
        return

    await state.update_data(runLevel=message.text)
    await message.answer(
        registrationTextInputLinkAccount,
        reply_markup=skipInput(),
    )
    # await Registration.next()
    await state.set_state(Registration.inputAccountLink)


@router.message(StateFilter(Registration.inputAccountLink))
async def cmdInputAccountLink(message: types.Message, state: FSMContext) -> None:
    if message.text == skipData()[0]:
        await state.update_data(accountLink="")
    else:
        await state.update_data(accountLink=message.text)
    await message.answer(
        registrationTextAdditionalPreQuestionText
        + "\n\n"
        + registrationTextAdditionalQuestionOne,
        reply_markup=createBinaryAnswer(),
    )
    # await Registration.next()
    await state.set_state(Registration.chooseRunLevelPartner)


@router.message(StateFilter(Registration.chooseRunLevelPartner))
async def cmdChooseRunLevelPartner(message: types.Message, state: FSMContext) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            exceptionText,
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(
        chooseRunLevelPartner=True if message.text == "Да" else False
    )
    await message.answer(
        registrationTextAdditionalQuestionTwo,
        reply_markup=createBinaryAnswer(),
    )
    # await Registration.next()
    await state.set_state(Registration.chooseGenderPartner)


@router.message(StateFilter(Registration.chooseGenderPartner))
async def cmdChooseGenderPartner(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    menu: ReplyKeyboardMarkup,
) -> None:
    if message.text not in getListBinaryAnswer():
        await message.answer(
            exceptionText,
            reply_markup=createBinaryAnswer(),
        )
        return

    await state.update_data(chooseGenderPartner=True if message.text == "Да" else False)
    await state.update_data(nickName=message.from_user.username)
    # It's for next step
    # await state.update_data(chooseOldPartner=False)

    # await message.answer(
    #     registrationTextAdditionalQuestionThree,
    #     reply_markup=createBinaryAnswer(),
    # )
    # await Registration.next()

    currectData = await state.get_data()
    userId = message.from_user.id
    userLinkTelegramAccount = message.from_user.url

    try:
        phoneNumber = message.contact.phone_number
    except:
        phoneNumber = ""

    # await db.addRegistrationData(
    #     data=prepareData(currectData, userId, phoneNumber, userLinkTelegramAccount)
    # )
    data = prepareData(currectData, userId, phoneNumber, userLinkTelegramAccount)
    await addRegistrationData(**data, session=session)
    # menu = await createMainMenu(userId=message.from_user.id)
    await message.answer(
        registrationTextFinalText,
        reply_markup=menu,
    )
    # await state.finish()
    await state.clear()


# async def cmdChooseOldPartner(message: types.Message, state: FSMContext) -> None:
#     if message.text not in getListBinaryAnswer():
#         await message.answer(
#             exceptionText,
#             reply_markup=createBinaryAnswer(),
#         )
#         return

#     await state.update_data(chooseOldPartner=True if message.text == "Да" else False)
#     currectData = await state.get_data()
#     userId = message.from_user.id
#     userLinkTelegramAccount = message.from_user.url
#     await db.addRegistrationData(
#         data=prepareData(currectData, userId, userLinkTelegramAccount)
#     )
#     menu = await createMainMenu(userId=message.from_user.id)
#     await message.answer(
#         registrationTextFinalText,
#         reply_markup=menu,
#     )
#     await state.finish()


def prepareData(currectData, userId, phoneNumber, userLinkTelegramAccount) -> dict:
    return {
        "id": uuid.uuid1(),
        "name": currectData["name"],
        "last_name": currectData["lastName"],
        "nick_name": (
            "нет" if len(currectData["nickName"]) < 1 else currectData["nickName"]
        ),
        "age": currectData["age"],
        "sex": currectData["sex"],
        "city": currectData["city"],
        "run_level": currectData["runLevel"],
        "account_link": currectData["accountLink"],
        "level_partner_need": currectData["chooseRunLevelPartner"],
        "any_gender": currectData["chooseGenderPartner"],
        # "use_old_partner": currectData["chooseOldPartner"],
        "meet_active": True,
        "id_telegram": userId,
        "phone_number": phoneNumber,
        "link_telegram": userLinkTelegramAccount,
        "active": True,
    }


# def registerHandlersRegistration(dp: Dispatcher) -> None:

#     dp.register_message_handler(
#         startRegistration,
#         Text(equals=["Учавствовать во встречах"], ignore_case=True),
#         state="*",
#     )
#     dp.register_message_handler(cmdInputName, state=Registration.inputName)
#     dp.register_message_handler(cmdInputAge, state=Registration.inputAge)
#     dp.register_message_handler(cmdChooseSex, state=Registration.chooseSex)
#     dp.register_message_handler(cmdChooseCity, state=Registration.chooseCity)
#     dp.register_message_handler(cmdInputCity, state=Registration.inputCity)
#     dp.register_message_handler(cmdChooseRunLevel, state=Registration.chooseRunLevel)
#     dp.register_message_handler(
#         cmdInputAccountLink, state=Registration.inputAccountLink
#     )
#     dp.register_message_handler(
#         cmdChooseRunLevelPartner, state=Registration.chooseRunLevelPartner
#     )
#     dp.register_message_handler(
#         cmdChooseGenderPartner, state=Registration.chooseGenderPartner
#     )
# dp.register_message_handler(
#     cmdChooseOldPartner, state=Registration.chooseOldPartner
# )
