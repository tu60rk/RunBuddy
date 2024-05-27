from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List


def create_main_menu(is_admin: int, is_registration: bool) -> ReplyKeyboardMarkup:

    lst_buttons = []
    if is_admin:
        lst_buttons.append(
            [
                KeyboardButton("Выгрузить отчет по ОС"),
            ]
        )
        return ReplyKeyboardMarkup(keyboard=lst_buttons, resize_keyboard=True)

    lst_buttons.append(
        [
            KeyboardButton("Учавствовать во встречах"),
        ]
    )
    if is_registration:
        lst_buttons.append(
            [
                KeyboardButton("Изменить данные"),
                KeyboardButton("Узнать мой статус по встречам"),
            ]
        )

    return ReplyKeyboardMarkup(keyboard=lst_buttons, resize_keyboard=True)


def choose_gender() -> ReplyKeyboardMarkup:
    lst_buttons = []
    lst_buttons.append([KeyboardButton("Мужской")])
    lst_buttons.append([KeyboardButton("Женский")])
    return ReplyKeyboardMarkup(keyboard=lst_buttons, resize_keyboard=True)


def choose_city() -> ReplyKeyboardMarkup:
    lst_buttons = []
    lst_buttons.append([KeyboardButton("Москва")])
    lst_buttons.append([KeyboardButton("Санкт-Петербург")])
    lst_buttons.append([KeyboardButton("Другой")])
    return ReplyKeyboardMarkup(keyboard=lst_buttons, resize_keyboard=True)


def choose_level() -> ReplyKeyboardMarkup:
    lst_buttons = []
    lst_buttons.append([KeyboardButton("Новичок")])
    lst_buttons.append([KeyboardButton("Любитель")])
    return ReplyKeyboardMarkup(keyboard=lst_buttons, resize_keyboard=True)


def create_binary_answer(for_lk: str = "") -> ReplyKeyboardMarkup:
    lst_buttons = []
    lst_buttons.append([KeyboardButton("Да"), KeyboardButton("Нет")])
    if for_lk:
        lst_buttons.append([KeyboardButton("⬅️ Меню личного кабинета")])
    return ReplyKeyboardMarkup(keyboard=lst_buttons, resize_keyboard=True)
