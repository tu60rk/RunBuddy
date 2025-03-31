from typing import cast, List
from datetime import datetime
import uuid
import pandas as pd

from sqlalchemy import select, or_
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, aliased
from uuid import UUID

from db.models import Registration, Meets, Comments


def isAdmin(userId: str, admins: List):
    if int(userId) in admins:
        return True
    return False


async def addRegistrationData(
    session: AsyncSession,
    id: UUID,
    name: str,
    last_name: str,
    nick_name: str,
    age: int,
    sex: str,
    city: str,
    run_level: str,
    account_link: str,
    any_gender: bool,
    meet_active: bool,
    id_telegram: str,
    link_telegram: str,
    active: bool,
    level_partner_need: bool | None = None,
    phone_number: str | None = None,
):
    stmt = upsert(Registration).values(
        {
            "id": id,
            "name": name,
            "last_name": last_name,
            "nick_name": nick_name,
            "age": age,
            "sex": sex,
            "city": city,
            "run_level": run_level,
            "account_link": account_link,
            "any_gender": any_gender,
            "meet_active": meet_active,
            "id_telegram": id_telegram,
            "link_telegram": link_telegram,
            "active": active,
            "level_partner_need": level_partner_need,
            "phone_number": phone_number,
        }
    )
    # stmt = stmt.on_conflict_do_update(
    #     index_elements=['telegram_id'],
    #     set_=dict(
    #         first_name=first_name,
    #         last_name=last_name,
    #     ),
    # )
    await session.execute(stmt)
    await session.commit()


async def isRegistration(userId: str, session: AsyncSession):
    stmt = select(Registration.id_telegram).where(
        Registration.id_telegram == str(userId)
    )
    result = await session.execute(stmt)
    return True if result.first() else False


async def isCanGetComment(userId: str, session: AsyncSession):
    subq = (
        select(Registration.id)
        .where(Registration.id_telegram == str(userId))
        .subquery()
    )
    stmt = select(Meets.id).where(
        or_(
            Meets.id_first_partner == subq,
            Meets.id_second_partner == subq,
        )
    )
    result = await session.execute(stmt)
    return True if result.first() else False


async def insertCommonComment(
    session: AsyncSession,
    id_telegram: str,
    comment: str,
):
    stmt = upsert(Meets).values(
        {
            "id": uuid.uuid1(),
            "id_telegram": id_telegram,
            "date_comment": datetime.now().date(),
            "comment": comment,
        }
    )
    await session.execute(stmt)
    await session.commit()


async def getMeetStatus(session: AsyncSession, userId: str):
    stmt = select(Registration.meet_active).where(
        Registration.id_telegram == str(userId)
    )
    result = await session.execute(stmt)
    return True if result.scalar() else False


async def getRegisteredUsers(session: AsyncSession, use_pandas: bool = False):
    stmt = select(
        Registration.id,
        Registration.name,
        Registration.last_name,
        Registration.nick_name,
        Registration.age,
        Registration.sex,
        Registration.city,
        Registration.run_level,
        Registration.account_link,
        Registration.level_partner_need,
        Registration.any_gender,
        Registration.meet_active,
        Registration.id_telegram,
        Registration.phone_number,
        Registration.link_telegram,
        Registration.active,
    )
    result = await session.execute(stmt)
    registeredUsers = result.all()
    if use_pandas:
        columns = [
            "id",
            "name",
            "lastName",
            "nickName",
            "age",
            "sex",
            "city",
            "runLevel",
            "accountLink",
            "levelPartnerNeed",
            "anyGender",
            "meetActive",
            "idTelegram",
            "phoneNumber",
            "linkTelegram",
            "active",
        ]
        registeredUsers = pd.DataFrame(registeredUsers, columns=columns)
    return registeredUsers


async def getMeetsQ(session: AsyncSession, use_pandas: bool = False):
    RegistrationFirst = aliased(Registration)
    RegistrationSecond = aliased(Registration)

    stmt = (
        select(
            Meets.id,
            Meets.id_first_partner,
            RegistrationFirst.nick_name,
            Meets.id_second_partner,
            RegistrationSecond.nick_name,
            Meets.date_algorithm,
            Meets.first_partner_meet,
            Meets.second_partner_meet,
        )
        .join(
            RegistrationFirst,
            Meets.id_first_partner == RegistrationFirst.id,
            isouter=True,
        )
        .join(
            RegistrationSecond,
            Meets.id_second_partner == RegistrationFirst.id,
            isouter=True,
        )
    )
    result = await session.execute(stmt)
    meets = result.all()
    if use_pandas:
        columns = [
            "id",
            "idFirstPartner",
            "nickNameUserOne",
            "idSecondPartner",
            "nickNameUserTwo",
            "algorithmDate",
            "userOneAnswer",
            "userTwoAnswer",
        ]
        meets = pd.DataFrame(meets, columns=columns)
    return meets


async def getCommentsQ(session: AsyncSession, use_pandas: bool = False):
    stmt = select(
        Registration.nick_name,
        Registration.phone_number,
        Comments.id,
        Comments.id_telegram,
        Comments.date_comment,
        Comments.comment,
    ).join(
        Registration,
        Comments.id_telegram == Registration.id_telegram,
        isouter=True,
    )
    result = await session.execute(stmt)
    comments = result.all()
    if use_pandas:
        columns = [
            "nickName",
            "phoneNumber",
            "id",
            "idTelegram",
            "dateComment",
            "comment",
        ]
        comments = pd.DataFrame(comments, columns=columns)
    return comments


async def getUsers(session: AsyncSession):
    stmt = select(Registration.id_telegram, Registration.active)
    result = await session.execute(stmt)
    return result.all()
    # return True if result.first() else False


async def setActive(session: AsyncSession, userId: str, flag: bool):
    stmt = select(Registration).where(Registration.id_telegram == str(userId))
    result = await session.execute(stmt)
    reg = result.scalar()
    if reg.active != flag:
        reg.active = flag
        await session.commit()

#     async def setActive(self, user_id: str, active: bool) -> None:
#         await self.database.execute(
#             "UPDATE registration SET active = :active WHERE id_telegram = :user_id",
#             values={"active": active, "user_id": user_id},
#         )

async def updateRegistrationData(session: AsyncSession, userId: int, columnName: str, data: str):
    stmt = select(Registration).where(Registration.id_telegram == str(userId))
    result = await session.execute(stmt)
    reg = result.scalar()
    if columnName == "meet_active":
        reg.meet_active = data
    if columnName == "any_gender":
        reg.any_gender = data
    if columnName == "level_partner_need":
        reg.level_partner_need = data
    if columnName == "account_link":
        reg.account_link = data
    if columnName == "run_level":
        reg.run_level = data
    if columnName == "city":
        reg.city = data
    await session.commit()

