from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# from utils.bd import DataBase
# from db.request import isAdmin, isRegistration, isCanGetComment
from settings.config import botTextSettings

# db = DataBase()


def buildButtons(stringNotSplited: str) -> list:
    stringNotSplited = stringNotSplited.split("|")
    if len(stringNotSplited) > 0:
        lstButtons = []
        for button in stringNotSplited:
            lstButtons.append([KeyboardButton(text=button)])
        return lstButtons
    return []


# async def createMainMenu(
#     userId: str, session: AsyncSession, admins: List
# ) -> ReplyKeyboardMarkup:

#     # isAdmin = db.isAdmin(userId=userId)
#     # isRegistration = await db.isRegistration(userId=userId)
#     # isCanGetComment = await db.isCanGetComment(userId=userId)

#     # isAdminR = isAdmin(userId=userId, admins=admins)
#     isRegistrationR = await isRegistration(userId=userId, session=session)
#     isCanGetCommentR = await isCanGetComment(userId=userId, session=session)
#     menuForAdmins = botTextSettings.menuForAdmins
#     menuForRegistered = botTextSettings.menuForRegistered
#     menuForUnRegistered = botTextSettings.menuForUnRegistered
#     menuForComment = botTextSettings.menuForComment

#     lstButtons = []
#     if isAdmin(userId=userId, admins=admins):
#         lstButtons = buildButtons(menuForAdmins)

#     if isRegistrationR:
#         lstButtons += buildButtons(menuForRegistered)
#     else:
#         lstButtons += buildButtons(menuForUnRegistered)

#     if isCanGetCommentR:
#         lstButtons += buildButtons(menuForComment)

#     return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)

async def createMainMenu(
        userId: str, session: AsyncSession, admins: List
):
    pass

def getListGender() -> list:
    gender = botTextSettings.gender
    return gender.split("|")


def chooseGender() -> ReplyKeyboardMarkup:
    lstButtons = []
    for gender in getListGender():
        lstButtons.append([KeyboardButton(text=gender)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListCities() -> list:
    cities = botTextSettings.cities
    return cities.split("|")


def chooseCity() -> ReplyKeyboardMarkup:
    lstButtons = []
    for city in getListCities():
        lstButtons.append([KeyboardButton(text=city)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListRunLevel() -> list:
    runLevels = botTextSettings.runLevels
    return runLevels.split("|")


def chooseRunLevel() -> ReplyKeyboardMarkup:
    lstButtons = []
    for level in getListRunLevel():
        lstButtons.append([KeyboardButton(text=level)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListBinaryAnswer() -> list:
    return ["Да", "Нет"]


def createBinaryAnswer(for_lk: str = "") -> ReplyKeyboardMarkup:
    lstButtons = []
    for binaryAnswer in getListBinaryAnswer():
        lstButtons.append([KeyboardButton(text=binaryAnswer)])
    if for_lk:
        lstButtons.append([KeyboardButton(text="⬅️ Меню личного кабинета")])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListColumnUpdateRegistration() -> list:
    changeDataMenu = botTextSettings.changeDataMenu
    return changeDataMenu.split("|")


def registrationUpdateData() -> ReplyKeyboardMarkup:
    lstButtons = []
    row = []
    for column in getListColumnUpdateRegistration():
        if len(row) == 2:
            lstButtons.append(row)
            row = []
        if column == getListColumnUpdateRegistration()[-1]:
            lstButtons.append(row)
        row.append(KeyboardButton(text=column))
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def skipData() -> list:
    return ["Пропустить ввод"]


def skipInput() -> ReplyKeyboardMarkup:
    lstButtons = []
    for skip in skipData():
        lstButtons.append([KeyboardButton(text=skip)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)
