# openapi https://github.com/openai/openai-python
from aiogram import types, F, Router, Bot
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.chat_action import ChatActionSender
from openai import AsyncOpenAI, APIConnectionError, RateLimitError, APIStatusError


from filters.registeredUser import registeredUser
from settings.config import textBotSettings, botSettings
from utils.buttons import (
    returnButton,
)

router = Router()
router.message.filter(registeredUser())


class chatGpt(StatesGroup):
    startChat = State()


@router.message(F.text == "Спросить совет (ChatGpt)", StateFilter(default_state))
async def startChatWithGpt(
    message: types.Message,
    state: FSMContext,
    botTextSettings: textBotSettings,
    throttlingChatGptCountLimit: int,
    botMainSettings: botSettings,
    menu: ReplyKeyboardMarkup,
) -> None:
    if throttlingChatGptCountLimit > botMainSettings.throttlingChatGptCountLimit:
        await message.answer(
            botTextSettings.limitOfCountRequest,
            reply_markup=menu,
        )
        await state.clear()
    else:
        await message.answer(
            botTextSettings.chatGptStart,
            reply_markup=returnButton(),
        )
        await state.set_state(chatGpt.startChat)


@router.message(StateFilter(chatGpt.startChat))
async def cmdChoose(
    message: types.Message,
    state: FSMContext,
    botTextSettings: textBotSettings,
    clientChatGpt: AsyncOpenAI,
    bot: Bot,
    throttlingChatGptCountLimit: int,
    botMainSettings: botSettings,
    menu: ReplyKeyboardMarkup,
) -> None:

    if throttlingChatGptCountLimit > botMainSettings.throttlingChatGptCountLimit:
        await message.answer(
            botTextSettings.limitOfCountRequest,
            reply_markup=menu,
        )
        await state.clear()
    else:
        async with ChatActionSender.typing(chat_id=message.from_user.id, bot=bot):
            try:
                response = await clientChatGpt.chat.completions.create(
                    model="meta-llama/llama-4-maverick:free",
                    messages=[
                        {
                            "role": "user",
                            "content": message.text,
                        }
                    ],
                    stream=True,
                )
                dataForSend = ""
                async for trunk in response:
                    if trunk.choices[0].delta.content:
                        dataForSend += trunk.choices[0].delta.content
                    else:
                        continue
                    if len(dataForSend) > 3600:
                        await message.answer(
                            dataForSend,
                            reply_markup=returnButton(),
                        )
                        dataForSend = ""
                if len(dataForSend) > 0:
                    await message.answer(
                        dataForSend,
                        reply_markup=returnButton(),
                    )
            except (APIConnectionError, RateLimitError, APIStatusError) as err:
                await message.answer(
                    "Что-то пошло не так... Попробуйте еще раз задать свой вопрос.",
                    reply_markup=returnButton(),
                )

        await state.set_state(chatGpt.startChat)
