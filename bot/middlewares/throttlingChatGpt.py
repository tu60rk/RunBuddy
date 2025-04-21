from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache
from typing import Any, Awaitable, Callable, Dict

from handlers.chatGpt import chatGpt
from settings.config import botMainSettings


CACHE = TTLCache(
    maxsize=10_000, ttl=botMainSettings.throttlingChatGptTimeLimit
)  # Максимальный размер кэша - 10000 ключей, а время жизни ключа в секундах


class ThrottlingChatGptMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        state = data.get("state")
        if state:
            state = await state.get_state()

        user: User = data.get("event_from_user")

        if state == chatGpt.startChat and event.message.text != "Вернуться в меню":
            if user.id in CACHE:
                requestCounter: int = CACHE[user.id]
                if requestCounter > int(botMainSettings.throttlingChatGptCountLimit):
                    data["throttlingChatGptCountLimit"] = requestCounter
                else:
                    CACHE[user.id] = requestCounter + 1
                    data["throttlingChatGptCountLimit"] = requestCounter + 1
            else:
                CACHE[user.id] = 1
                data["throttlingChatGptCountLimit"] = 1
        if event.message.text == "Спросить совет (ChatGpt)":
            if user.id not in CACHE:
                data["throttlingChatGptCountLimit"] = 0
            else:
                data["throttlingChatGptCountLimit"] = CACHE[user.id]
        return await handler(event, data)
