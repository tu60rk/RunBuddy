import pandas as pd
import uuid

from typing import Union
from datetime import datetime
from aiogram.utils.exceptions import ChatNotFound

from settings.config import botTextSettings, botMainSettings


dontFindPartner = botTextSettings.dontFindPartner.replace("|", "\n")
findPartner = botTextSettings.findPartner.replace("|", "\n")


isTest = botMainSettings.isTest
ageRange = botMainSettings.ageRange


# Алгоритм

# Найти всех активных участников - список -ids
# Используем while до тех пор, пока список не станет пустым
# Берем первого из списка. Берем его настройки:
# город
# если не любой гендер, то гендер
# если не любой уровень, то уровень
# если есть параметр AgeRange, то смотрим возраст в пределах
# Ищем в таблице по настройкам партнера
# найден
#   - проверяем, что они впервые встречаются
#       - формируем сообщение обоим и удаляем из списка
#   - ищем дальше, пока не найдем
# не найден - формируем сообщение, что не найден и предлагаем ранних с ним бегающих - ВАЖНО если они активные и оба оказались в этой выборке!
# Если список оказался пуст - выходим


async def getActiveUsers(db) -> pd.DataFrame:
    return await db.getActiveUsers()


def getUserSettings(
    acitveUsers: pd.DataFrame, idUser: uuid.UUID
) -> Union[str, bool, bool]:
    acitveUsers = acitveUsers[acitveUsers.id == idUser]
    return (
        acitveUsers.city.values.tolist()[0],
        acitveUsers.anyGender.values.tolist()[0],
        acitveUsers.levelPartnerNeed.values.tolist()[0],
        acitveUsers.age.values.tolist()[0],
        acitveUsers.sex.values.tolist()[0],
        acitveUsers.runLevel.values.tolist()[0],
    )


def getUserData(acitveUsers: pd.DataFrame, idUser: uuid.UUID):
    acitveUsers = acitveUsers[acitveUsers.id == idUser]
    return (
        acitveUsers.idTelegram.values.tolist()[0],
        acitveUsers.name.values.tolist()[0],
        acitveUsers.linkTelegram.values.tolist()[0],
        acitveUsers.accountLink.values.tolist()[0],
    )


def getUsersPartners(
    idUser: uuid.UUID, acitveUsers: pd.DataFrame, removeIdsList: list
) -> list:

    (
        userCity,
        userPartnerGender,
        userPartnerLevel,
        userAge,
        userGender,
        userLevel,
    ) = getUserSettings(acitveUsers=acitveUsers, idUser=idUser)
    # only the same gender and run level
    patnres = acitveUsers[
        (acitveUsers.city == userCity)
        & (acitveUsers.age >= userAge - ageRange)
        & (acitveUsers.age <= userAge + ageRange)
        & (~acitveUsers.id.isin(removeIdsList))
        & (acitveUsers.id != idUser)
    ]

    patnres = patnres[
        (patnres.anyGender == True)
        | ((patnres.anyGender == False) & (patnres.sex == userGender))
    ]
    if not userPartnerGender:
        patnres = patnres[(patnres.sex == userGender)]
    patnres = patnres[
        (patnres.levelPartnerNeed == False)
        | ((patnres.levelPartnerNeed == True) & (patnres.runLevel == userLevel))
    ]
    if userPartnerLevel:
        patnres = patnres[(patnres.runLevel == userLevel)]

    if not patnres.empty:
        return patnres.id.values.tolist()


async def getPartner(
    db, userId: str, findUsers: list, dataForTest: pd.DataFrame = None
):
    for newPartner in findUsers:
        if isTest:
            isNewPartner = True
            df = dataForTest[
                (
                    (dataForTest.partnerFirst == userId)
                    & (dataForTest.partnerSecond == newPartner)
                )
                | (
                    (dataForTest.partnerFirst == newPartner)
                    & (dataForTest.partnerSecond == userId)
                )
            ]
            if not df.empty:
                isNewPartner = False
        else:
            isNewPartner = await db.isNewPartner(userId=userId, newPartner=newPartner)
        if isNewPartner:
            return newPartner


async def sendSimpleNotification(bot, idUserTelegram: str) -> None:
    await bot.send_message(
        idUserTelegram,
        dontFindPartner,
    )


async def sendNotification(bot, acitveUsers, idUser, findPartnerId):

    userIdTelegram, nameUser, userLinkTelegram, userLinkSocial = getUserData(
        acitveUsers=acitveUsers, idUser=idUser
    )
    (
        findUserIdTelegram,
        nameFindUser,
        findUserLinkTelegram,
        findUserLinkSocial,
    ) = getUserData(acitveUsers=acitveUsers, idUser=findPartnerId)

    addText = (
        "\nСсылка на соц. сеть - " + findUserLinkSocial if findUserLinkSocial else ""
    )
    addTextPartner = (
        "\nСсылка на соц. сеть - " + userLinkSocial if userLinkSocial else ""
    )

    await bot.send_message(
        userIdTelegram,
        findPartner
        + f"""\nВот ссылка на него в телеграмме - {findUserLinkTelegram}\nИмя - {nameFindUser}{addText}""",
    )
    try:
        await bot.send_message(
            findUserIdTelegram,
            findPartner
            + f"""\nВот ссылка на него в телеграмме - {userLinkTelegram}\nИмя - {nameUser}{addTextPartner}""",
        )
    except ChatNotFound:
        pass


async def oldPartnerAlgorithm(
    bot,
    db,
    oldPartners: list,
    acitveUsers: pd.DataFrame,
    dataForTest: pd.DataFrame = None,
) -> None:
    while len(oldPartners) > 0:
        idUser = oldPartners[0]
        idUserTelegram = acitveUsers[
            acitveUsers.id == idUser
        ].idTelegram.values.tolist()[0]
        oldPartners.remove(idUser)

        # find old partner
        findPartner = False
        for oldPartner in oldPartners:
            if isTest:
                isNewPartner = True
                df = dataForTest[
                    (
                        (dataForTest.partnerFirst == idUser)
                        & (dataForTest.partnerSecond == oldPartner)
                    )
                    | (
                        (dataForTest.partnerFirst == oldPartner)
                        & (dataForTest.partnerSecond == idUser)
                    )
                ]
                if not df.empty:
                    isNewPartner = False
            else:
                isNewPartner = await db.isNewPartner(
                    userId=idUser, newPartner=oldPartner
                )

            if not isNewPartner:
                findPartner = True
                oldPartners.remove(oldPartner)
                if not isTest:
                    await db.insertMeet(
                        idUser=idUser,
                        findPartnerId=oldPartner,
                        algothmTime=datetime.now().date(),
                    )
                await sendNotification(
                    bot=bot,
                    acitveUsers=acitveUsers,
                    idUser=idUser,
                    findPartnerId=oldPartner,
                )
                break
        # not find
        if not findPartner:
            await sendSimpleNotification(bot=bot, idUserTelegram=idUserTelegram)


async def generalAlgoritm(bot, db, acitveUsers=None, partners=None):

    if not isTest:
        acitveUsers = await getActiveUsers(db=db)

    idsList = acitveUsers.id.values.tolist()
    removeIdsList = []
    # oldPartners = []

    while len(idsList) > 0:

        idUser = idsList[0]
        idUserTelegram = acitveUsers[
            acitveUsers.id == idUser
        ].idTelegram.values.tolist()[0]
        # useOldPartner = acitveUsers[
        #     acitveUsers.id == idUser
        # ].chooseOldPartner.values.tolist()[0]
        findUsers = getUsersPartners(
            acitveUsers=acitveUsers, idUser=idUser, removeIdsList=removeIdsList
        )

        idsList.remove(idUser)
        removeIdsList.append(idUser)

        if findUsers:
            findPartnerId = await getPartner(
                db=db, userId=idUser, findUsers=findUsers, dataForTest=partners
            )  # выдает id партнера или пустоту
            if findPartnerId:
                idsList.remove(findPartnerId)
                removeIdsList.append(findPartnerId)
                # insert
                if not isTest:
                    await db.insertMeet(
                        idUser=idUser,
                        findPartnerId=findPartnerId,
                        algothmTime=datetime.now().date(),
                    )
                # send notification
                await sendNotification(
                    bot=bot,
                    acitveUsers=acitveUsers,
                    idUser=idUser,
                    findPartnerId=findPartnerId,
                )
                continue
        # партнеры не найдены по критериям
        # отправляем нотификацию или ищем по старым партнерам.
        # if useOldPartner:
        #     oldPartners.append(idUser)
        # else:
        await sendSimpleNotification(bot=bot, idUserTelegram=idUserTelegram)

    # Use algorithm of old partner
    # if len(oldPartners) > 0:
    #     await oldPartnerAlgorithm(
    #         bot=bot,
    #         db=db,
    #         oldPartners=oldPartners,
    #         acitveUsers=acitveUsers,
    #         dataForTest=partners,
    #     )


# print("Test?", isTest)
# if isTest:
#     from utils.testCoreData import (
#         TestData01,
#         TestData02,
#         TestData03,
#         TestData04,
#         TestData05,
#         TestData06,
#         TestData07,
#         TestData08,
#         TestData09,
#         TestData10,
#     )

#     async def testSendSimpleNotification(bot, idUserTelegram):
#         print(f"For user {idUserTelegram} don't find a partner")

#     async def testSendNotification(bot, acitveUsers, idUser, findPartnerId):
#         userIdTelegram, nameUser, userLinkTelegram, userLinkSocial = getUserData(
#             acitveUsers=acitveUsers, idUser=idUser
#         )
#         (
#             findUserIdTelegram,
#             nameFindUser,
#             findUserLinkTelegram,
#             findUserLinkSocial,
#         ) = getUserData(acitveUsers=acitveUsers, idUser=findPartnerId)

#         print(
#             f"""Привет!👋
# Мы нашли тебе партнера по бегу!
# Вот ссылка на него в телеграмме - {findUserLinkTelegram}
# Имя - {nameFindUser}
# Ссылка на соц. сеть - {findUserLinkSocial}"""
#         )

#         print(
#             f"""Привет!👋
# Мы нашли тебе партнера по бегу!
# Вот ссылка на него в телеграмме - {userLinkTelegram}
# Имя - {nameUser}
# Ссылка на соц. сеть - {userLinkSocial}"""
#         )

#     sendSimpleNotification = testSendSimpleNotification
#     sendNotification = testSendNotification
#     bot = ""

#     # test of base algothm
#     for func in [
#         TestData01,
#         TestData02,
#         TestData03,
#         TestData04,
#         TestData05,
#         TestData06,
#         TestData07,
#     ]:
#         acitveUsers, partners = func()
#         asyncio.run(
#             generalAlgoritm(bot=bot, acitveUsers=acitveUsers, partners=partners)
#         )

#     # test of patneralgorithm
#     for func in [TestData08, TestData09, TestData10]:
#         acitveUsers, partners = func()
#         asyncio.run(
#             generalAlgoritm(bot=bot, acitveUsers=acitveUsers, partners=partners)
#         )
