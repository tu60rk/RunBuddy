from aiogram.types import Message
from aiogram.filters import BaseFilter
from sqlalchemy.ext.asyncio import AsyncSession

from db.request import isRegistration


class registeredUser(BaseFilter):
    async def __call__(
        self, message: Message, session: AsyncSession
    ) -> bool | dict[str, list[int]]:
        isRegistrationR = await isRegistration(
            userId=message.from_user.id, session=session
        )
        return isRegistrationR
