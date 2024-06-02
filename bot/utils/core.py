import pandas as pd
import os
import uuid

from typing import Union
from datetime import datetime

from utils.bd import DataBase

db = DataBase()
ageRange = os.getenv("ageRange")
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

async def getActiveUsers() -> pd.DataFrame:
    return await db.getActiveUsers()


def getUserSettings(acitveUsers: pd.DataFrmae, idUser: uuid.UUID) -> Union[str,bool,bool]:
    acitveUsers = acitveUsers[acitveUsers.id == idUser]
    return (
        acitveUsers.city.values.tolist()[0], 
        acitveUsers.anyGender.values.tolist()[0], 
        acitveUsers.levelPartnerNeed.values.tolist()[0],
        acitveUsers.age.values.tolist()[0],
        acitveUsers.sex.values.tolist()[0],
        acitveUsers.runLevel.values.tolist()[0],
    )

def getUserData():
    pass

def getUsersPartners(idUser: uuid.UUID, acitveUsers: pd.DataFrame, removeIdsList: list) -> list:
    
    userCity, userPartnerGender, userPartnerLevel, userAge, userGender, userLevel = getUserSettings(acitveUsers=acitveUsers,idUser=idUser)
    # only the same gender and run level
    patnres = acitveUsers[
        (acitveUsers.city == userCity) &
        (acitveUsers.age >= userAge - ageRange) &
        (acitveUsers.age <= userAge + ageRange) &
        (~acitveUsers.id.isin(removeIdsList)) &
        (~acitveUsers.id != idUser)
    ]
    if not userPartnerGender:
        patnres = patnres[
            (patnres.sex == userGender)
        ]
    if userPartnerLevel:
        patnres = patnres[
            (patnres.runLevel == userLevel)
        ]
    
    if not patnres.empty:
        return patnres.id.values.tolist()

async def getPartner(userId, findUsers):
    for newPartner in findUsers:
        isNewPartner = await db.isNewPartner(userId=userId, newPartner=newPartner)
        if isNewPartner:
            return newPartner

async def sendNotification(bot, acitveUsers, idUser, findPartnerId):
    
    userIdTelegram, nameUser, userLinkTelegram, userLinkSocial = getUserData(acitveUsers=acitveUsers, idUser=idUser)
    findUserIdTelegram, nameFindUser, findUserLinkTelegram, findUserLinkSocial = getUserData(acitveUsers=acitveUsers, idUser=findPartnerId)

    await bot.send_message(
        userIdTelegram, 
        f"""Привет!👋
Мы нашли тебе партнера по бегу!
Вот ссылка на него в телеграмме - {findUserLinkTelegram}
Имя - {nameFindUser}
Ссылка на соц. сеть - {findUserLinkSocial}"""
    )
    await bot.send_message(
        findUserIdTelegram,
        f"""Привет!👋
Мы нашли тебе партнера по бегу!
Вот ссылка на него в телеграмме - {userLinkTelegram}
Имя - {nameUser}
Ссылка на соц. сеть - {userLinkSocial}"""
    )

async def generalAlgoritm(bot):
    acitveUsers = getActiveUsers()
    idsList = acitveUsers.id.values.tolist()
    removeIdsList =[]
    oldPartners = []

    while len(idsList) != 0:
        if len(idsList) == 1:
                # отправляем инфу, что не нашли партнера.
            break
            
        idUser = idsList[0]
        idUserTelegram = acitveUsers[acitveUsers.id == idUser].idTelegram.values.tolsit()[0]
        findUsers = getUsersPartners(
            acitveUsers=acitveUsers,
            idUser=idUser,
            removeIdsList=removeIdsList
        )
        if findUsers:
            findPartnerId  = await getPartner(findUsers) # выдает id партнера или пустоту
            if findPartnerId:
                idsList.remove(idUser)
                idsList.remove(findPartnerId)
                removeIdsList.append(idUser)
                removeIdsList.append(findPartnerId)
                # insert
                await db.insertMeet(idUser=idUser, findPartnerId=findPartnerId, algothmTime=datetime.now())
                # send notification
                await sendNotification(bot=bot, acitveUsers=acitveUsers, idUser=idUser, findPartnerId=findPartnerId)
                continue
            else:
                oldPartners.append(idUser)

                idsList.remove(idUser)
                removeIdsList.append(idUser)
                continue

        # партнеры не найдены по критериям
        # отправляем нотификацию
        else:
            # send notification
            idsList.remove(idUser)
            removeIdsList.append(idUser)
            await bot.send_message(
                idUserTelegram,
    """Привет!👋
К сожалению, мы не подобрали тебе партнера по бегу :(
мы привлекаем новых пользователей и в будущем такого быть не должно."""

            )
            continue
    
    if len(oldPartners) > 0:
        if len(oldPartners) == 1:
            # партнеры не найдены по критериям
            # отправляем нотификацию
            pass

        # выбрать четное кол-во пользователей
        # отправить им сообщение, что хотели бы вы пробежаться со старым партнером?
        # ожидаем подтверждения от другого пользователя


            
            

