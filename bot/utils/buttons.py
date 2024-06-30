import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

from utils.bd import DataBase

db = DataBase()


async def createMainMenu(userId: str) -> ReplyKeyboardMarkup:

    isAdmin = db.isAdmin(userId=userId)
    isRegistration = await db.isRegistration(userId=userId)

    lstButtons = []
    if isAdmin:
        lstButtons.append(
            [
                KeyboardButton("Выгрузить отчет по ОС"),
            ]
        )
        return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)

    if isRegistration:
        lstButtons.append(
            [
                KeyboardButton("Изменить данные"),
                KeyboardButton("Узнать мой статус по встречам"),
            ]
        )
    else:
        lstButtons.append(
            [
                KeyboardButton("Учавствовать во встречах"),
            ]
        )

    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListGender() -> list:
    gender = os.getenv("gender", "")
    return gender.split("|")


def chooseGender() -> ReplyKeyboardMarkup:
    lstButtons = []
    for gender in getListGender():
        lstButtons.append([KeyboardButton(gender)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListCities() -> list:
    cities = os.getenv("cities", "")
    return cities.split("|")


def chooseCity() -> ReplyKeyboardMarkup:
    lstButtons = []
    for city in getListCities():
        lstButtons.append([KeyboardButton(city)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListRunLevel() -> list:
    runLevels = os.getenv("runLevels", "")
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
    changeDataMenu = os.getenv("changeDataMenu", "")
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
