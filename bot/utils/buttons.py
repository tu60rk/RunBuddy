from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

from utils.bd import DataBase

db = DataBase()

async def createMainMenu(userId:str) -> ReplyKeyboardMarkup:

    isAdmin = await db.isAdmin(userId=userId)
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
    return ["Мужской", "Женский"]


def chooseGender() -> ReplyKeyboardMarkup:
    lstButtons = []
    for gender in getListGender():
        lstButtons.append([KeyboardButton(gender)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListCities() -> list:
    return ["Москва", "Санкт-Петербург", "Другой"]


def chooseCity() -> ReplyKeyboardMarkup:
    lstButtons = []
    for city in getListCities():
        lstButtons.append([KeyboardButton(city)])
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)


def getListRunLevel() -> list:
    return ["Новичок", "Любитель"]


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
    return ["Город", "Уровень подготовки", "Уровень подготовки напарника", "Статус встреч", "Ссылку на аккаунт", "Бег с любым полом"]


def registrationUpdateData() -> ReplyKeyboardMarkup:
    lstButtons = []
    row = []
    for column in getListColumnUpdateRegistration():
        if len(row) == 2:
            lstButtons.append(row)
            row = [KeyboardButton(column)]
        elif column == getListColumnUpdateRegistration()[-1]:
            row.append(KeyboardButton(column))
            lstButtons.append(row)
        else:
            row.append(column)
    return ReplyKeyboardMarkup(keyboard=lstButtons, resize_keyboard=True)
