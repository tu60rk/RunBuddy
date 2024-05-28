from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List


def createMainMenu(isAdmin: bool, isRegistration: bool) -> ReplyKeyboardMarkup:

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
