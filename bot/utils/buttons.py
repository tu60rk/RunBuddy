import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

from utils.bd import DataBase
from settings.config import botTextSettings

db = DataBase()

def buildButtons(stringNotSplited: str) -> list:
    stringNotSplited = stringNotSplited.split("|")
    if len(stringNotSplited) > 0:
        lstButtons = []
        for adminButton in stringNotSplited:
            lstButtons.append([adminButton])
        return lstButtons
    return []
        


async def createMainMenu(userId: str) -> ReplyKeyboardMarkup:

    isAdmin = db.isAdmin(userId=userId)
    isRegistration = await db.isRegistration(userId=userId)
    isCanGetComment = await db.isCanGetComment(userId=userId)
    menuForAdmins = botTextSettings.menuForAdmins
    menuForRegistered = botTextSettings.menuForRegistered
    menuForUnRegistered = botTextSettings.menuForUnRegistered
    menuForComment = botTextSettings.menuForComment

    lstButtons = []
    if isAdmin:
        lstButtons = buildButtons(menuForAdmins)

    if isRegistration:
        lstButtons += buildButtons(menuForRegistered)
    else:
        lstButtons += buildButtons(menuForUnRegistered)
    
    if isCanGetComment:
        lstButtons += buildButtons(menuForComment)


    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListGender() -> list:
    gender = botTextSettings.gender
    return gender.split("|")


def chooseGender() -> ReplyKeyboardMarkup:
    lstButtons = []
    for gender in getListGender():
        lstButtons.append([KeyboardButton(gender)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListCities() -> list:
    cities = botTextSettings.cities
    return cities.split("|")


def chooseCity() -> ReplyKeyboardMarkup:
    lstButtons = []
    for city in getListCities():
        lstButtons.append([KeyboardButton(city)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListRunLevel() -> list:
    runLevels = botTextSettings.runLevels
    return runLevels.split("|")


def chooseRunLevel() -> ReplyKeyboardMarkup:
    lstButtons = []
    for level in getListRunLevel():
        lstButtons.append([KeyboardButton(level)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListBinaryAnswer() -> list:
    return ["Да", "Нет"]


def createBinaryAnswer(for_lk: str = "") -> ReplyKeyboardMarkup:
    lstButtons = []
    for binaryAnswer in getListBinaryAnswer():
        lstButtons.append([KeyboardButton(binaryAnswer)])
    if for_lk:
        lstButtons.append([KeyboardButton("⬅️ Меню личного кабинета")])
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
        row.append(column)
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def skipData() -> list:
    return ["Пропустить ввод"]


def skipInput() -> ReplyKeyboardMarkup:
    lstButtons = []
    for skip in skipData():
        lstButtons.append([KeyboardButton(skip)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)
