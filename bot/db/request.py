from typing import List
from datetime import datetime, date
import uuid
import pandas as pd

from sqlalchemy import select, or_, and_, union_all, func, case, update
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
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
    stmt = upsert(Comments).values(
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


async def setActive(session: AsyncSession, userId: str, flag: bool):
    stmt = select(Registration).where(Registration.id_telegram == str(userId))
    result = await session.execute(stmt)
    reg = result.scalar()
    if reg.active != flag:
        reg.active = flag
        await session.commit()


async def updateRegistrationData(
    session: AsyncSession, userId: int, columnName: str, data: str
):
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


async def getActiveUsers(session: AsyncSession, use_pandas: bool = False):
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
    ).where(Registration.meet_active == True)
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


async def isNewPartner(session: AsyncSession, userId: str, newPartner: str) -> bool:
    stmt = select(Meets.id).where(
        or_(
            and_(
                Meets.id_first_partner == userId,
                Meets.id_second_partner == newPartner,
            ),
            and_(
                Meets.id_first_partner == newPartner,
                Meets.id_second_partner == userId,
            ),
        )
    )
    result = await session.execute(stmt)
    return False if result.first() else True


async def insertMeet(
    session: AsyncSession,
    idUser: int,
    findPartnerId: int,
    algothmTime: date,
) -> None:
    stmt = upsert(Meets).values(
        {
            "id": uuid.uuid1(),
            "id_first_partner": idUser,
            "id_second_partner": findPartnerId,
            "date_algorithm": algothmTime,
        }
    )
    await session.execute(stmt)
    await session.commit()


async def getUsersWhichDontAnswer(session: AsyncSession, use_pandas=False):
    # get three last dates
    stmt = select(Meets.date_algorithm).order_by(Meets.date_algorithm.desc()).limit(3)
    # list_dates = await session.scalars(stmt).all()
    result_tmp = await session.execute(stmt)
    list_dates = [r for r, in result_tmp]
    if len(list_dates) > 0:
        q1 = select(
            Meets.id_first_partner.label("id"), Meets.first_partner_meet.label("meeted")
        ).where(Meets.date_algorithm.in_(list_dates))
        q2 = select(
            Meets.id_second_partner.label("id"),
            Meets.second_partner_meet.label("meeted"),
        ).where(Meets.date_algorithm.in_(list_dates))
        q3 = union_all(q1, q2)
        final_query = (
            select(
                q3.c.id,
                Registration.nick_name,
                func.max(case((q3.c.meeted != False, 1), else_=1)),
            )
            .join(
                Registration,
                q3.c.id == Registration.id,
                isouter=True,
            )
            .group_by(q3.c.id, Registration.nick_name)
            .having(func.max(case((q3.c.meeted != False, 1), else_=1)) >= 3)
        )

        result = await session.execute(final_query)
        usersWhichDontAnswer = result.all()
        if use_pandas:
            columns = ["ids", "nickName", "summed"]
            usersWhichDontAnswer = pd.DataFrame(usersWhichDontAnswer, columns=columns)

        return usersWhichDontAnswer


async def getMaxDateMeet(session: AsyncSession) -> date:
    stmt = select(func.max(Meets.date_algorithm).label("date_algorithm"))
    result = await session.execute(stmt)
    tmp_res = result.scalar()
    if tmp_res:
        return tmp_res
    return None


async def getLastMeet(session: AsyncSession, maxDateMeet: date) -> str:
    q1 = (
        select(Registration.id_telegram)
        .join(Meets, Registration.id == Meets.id_first_partner)
        .where(Meets.date_algorithm == maxDateMeet)
    )
    q2 = (
        select(Registration.id_telegram)
        .join(Meets, Registration.id == Meets.id_second_partner)
        .where(Meets.date_algorithm == maxDateMeet)
    )
    q3 = union_all(q1, q2)
    final_query = select(q3.c.id_telegram)
    result = await session.execute(final_query)
    reg = result.scalars().all()
    if reg:
        return reg
    return None


async def getUserRegistrationId(session: AsyncSession, idTelegram: int) -> UUID:
    stmt = select(Registration.id).where(Registration.id_telegram == str(idTelegram))
    result = await session.execute(stmt)
    reg = result.scalar()
    if reg:
        return reg
    return None


async def getIdMeetLastMeet(
    session: AsyncSession, idUser: UUID, dateAlgorithm: date
) -> UUID:
    stmt = select(Meets.id).where(
        and_(
            or_(
                Meets.id_first_partner == idUser,
                Meets.id_second_partner == idUser,
            ),
            Meets.date_algorithm == dateAlgorithm,
        )
    )
    result = await session.execute(stmt)
    reg = result.scalar()
    if reg:
        return reg
    return None


async def getMeetById(
    session: AsyncSession, meetId: UUID, use_pandas: bool = False
) -> pd.DataFrame:
    stmt = select(
        Meets.id,
        Meets.id_first_partner,
        Meets.id_second_partner,
        Meets.date_algorithm,
        Meets.first_partner_meet,
        Meets.second_partner_meet,
    ).where(Meets.id == meetId)
    result = await session.execute(stmt)
    meetById = result.all()
    if use_pandas:
        columns = [
            "id",
            "idUserOne",
            "idUserTwo",
            "algorithmDate",
            "userOneAnswer",
            "userTwoAnswer",
        ]
        meetById = pd.DataFrame(meetById, columns=columns)
    return meetById


async def updateMeetData(
    session: AsyncSession, meetId: UUID, columnName: str, data: bool
) -> None:
    if columnName == "first_partner_meet":
        stmt = update(Meets).where(Meets.id == meetId).values(first_partner_meet=data)
    else:
        stmt = update(Meets).where(Meets.id == meetId).values(second_partner_meet=data)

    await session.execute(stmt)
    await session.commit()
