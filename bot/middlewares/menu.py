from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, ReplyKeyboardMarkup
from typing import Callable, Awaitable, Dict, Any

from db.request import (
    isCanGetComment,
    isRegistration,
    isAdmin,
)
from handlers.registration import Registration
from utils.buttons import buildButtons


class MenuMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user is not None:
            state = data.get('state')
            
            if state:
                state = await state.get_state()
            userId = user.id
            session = data.get("session")
            admins = data.get("admins")
            menuForAdmins = data.get("botTextSettings").menuForAdmins
            menuForRegistered = data.get("botTextSettings").menuForRegistered
            menuForUnRegistered = data.get("botTextSettings").menuForUnRegistered
            menuForComment = data.get("botTextSettings").menuForComment

            isRegistrationR = await isRegistration(userId=userId, session=session)
            isCanGetCommentR = await isCanGetComment(userId=userId, session=session)

            lstButtons = []
            if isAdmin(userId=userId, admins=admins):
                lstButtons = buildButtons(menuForAdmins)

            if isRegistrationR or state == Registration.chooseGenderPartner:
                lstButtons += buildButtons(menuForRegistered)
            else:
                lstButtons += buildButtons(menuForUnRegistered)

            if isCanGetCommentR:
                lstButtons += buildButtons(menuForComment)

            data["menu"] = ReplyKeyboardMarkup(
                keyboard=lstButtons, resize_keyboard=True
            )
            return await handler(event, data)
        return
