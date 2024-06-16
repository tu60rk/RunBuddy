import pandas as pd
import os
import logging
import uuid

from datetime import datetime
from typing import List, Union
from databases import Database
from sqlalchemy import column

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levselname)s - %(name)s - %(message)s",
)

DB_URL = os.getenv("DATABASE_URL")
DB_URL = "postgres://run:RunBuddyPassword@db:5432/run_database"
ADMINS = os.getenv("ADMINS")
if ADMINS:
    admins = [int(i) for i in ADMINS.split(",")]
else:
    admins = []


class NotSelectInSql(Exception):
    pass


class NotInsertInSql(Exception):
    pass


class DataBase:
    database = Database(DB_URL)

    async def getActiveUsers(self) -> pd.DataFrame:
        columns = [
            "id",
            "name",
            "lastName",
            "age",
            "sex",
            "city",
            "runLevel",
            "accountLink",
            "levelPartnerNeed",
            "anyGender",
            "chooseOldPartner",
            "meetActive",
            "idTelegram",
            "linkTelegram",
        ]
        df = await self.get_df(
            f"""SELECT 
            id
            ,name
            ,last_name
            ,age
            ,sex
            ,city
            ,run_level
            ,account_link
            ,level_partner_need
            ,any_gender
            ,use_old_partner
            ,meet_active
            ,id_telegram
            ,link_telegram
         FROM registration WHERE meet_active is true""",
            columns=columns,
        )
        return df

    async def getUserRegistrationId(self, idTelegram: str):
        columns = ["ids"]
        df = await self.get_df(f"SELECT id  FROM registration WHERE id_telegram = {int(idTelegram)}", columns=columns)
        return df.ids.values[0]

    async def getMeetStatus(self, userId: str) -> list:
        results = await self.database.fetch_all(
            f"SELECT meet_active FROM registration WHERE id_telegram = {int(userId)}"
        )
        return [list(result.values()) for result in results]

    async def deleteRegistrationDataByUser(self, userId: str) -> None:
        await self.database.execute(
            "DELETE FROM registration WHERE id_telegram = :id_telegram",
            values={"id_telegram": int(userId)},
        )

    async def addRegistrationData(self, data: dict) -> None:
        await self.database.execute(
            """INSERT INTO registration (
                id
                ,name
                ,last_name
                ,age
                ,sex
                ,city
                ,run_level
                ,account_link
                ,level_partner_need
                ,any_gender
                ,use_old_partner
                ,meet_active
                ,id_telegram
                ,link_telegram
            ) VALUES (
                 :id
                ,:name
                ,:last_name
                ,:age
                ,:sex
                ,:city
                ,:run_level
                ,:account_link
                ,:level_partner_need
                ,:any_gender
                ,:use_old_partner
                ,:meet_active
                ,:id_telegram
                ,:link_telegram
            )
        """,
            values={
                "id": data["id"],
                "name": data["name"],
                "last_name": data["last_name"],
                "age": data["age"],
                "sex": data["sex"],
                "city": data["city"],
                "run_level": data["run_level"],
                "account_link": data["account_link"],
                "level_partner_need": data["level_partner_need"],
                "any_gender": data["any_gender"],
                "use_old_partner": data["use_old_partner"],
                "meet_active": data["meet_active"],
                "id_telegram": data["id_telegram"],
                "link_telegram": data["link_telegram"],
            },
        )

    async def updateRegistrationData(
        self, userId: str, columnName: str, data: str
    ) -> None:
        await self.database.execute(
            f"""
            UPDATE registration SET {columnName} = :column_name
            WHERE id_telegram = :user_id
        """,
            values={"column_name": data, "user_id": int(userId)},
        )

    def isAdmin(self, userId: str) -> bool:
        if int(userId) in admins:
            return True
        return False

    async def isRegistration(self, userId: str) -> bool:
        results = await self.database.fetch_all(
            "SELECT * FROM registration WHERE id_telegram = :user_id",
            values={"user_id": int(userId)},
        )
        return bool(len([list(result.values()) for result in results]))

    async def isNewPartner(self, userId: str, newPartner: str) -> bool:
        results = await self.database.fetch_all(
            """
            with groupMeet as (
                select id_meet, max(find_partner) as mxFindPartner, min(find_partner) as mnFindPartner
                from comments
                where id_registration in (:id_first_partner, :id_second_partner)
            )   
               SELECT m.id 
               FROM meets m LEFT JOIN groupMeet g on m.id = g.id_meet 
               WHERE ((m.id_first_partner = :id_first_partner and m.id_second_partner = :id_second_partner) or
                     (m.id_first_partner = :id_second_partner and m.id_second_partner = :id_first_partner)) 
                     and g.mxFindPartner is true 
                     and g.mnFindPartner is true
            """,
            values={
                "id_first_partner": int(userId),
                "id_second_partner": int(newPartner),
            },
        )
        if bool(len([list(result.values()) for result in results])):
            return False
        return True
    
    async def isNewPartnerForPartnerAlgorithm(self, userId: str, newPartner: str) -> bool:
        results = await self.database.fetch_all(
            """SELECT m.id 
               FROM meets m 
               LEFT JOIN comments c1 on m.id = c1.id_meet and m.id_first_partner = c1.id_registration
               LEFT JOIN comments c2 on m.id = c2.id_meet and m.id_second_partner = c2.id_registration
               id_registration id_partner
               WHERE ((m.id_first_partner = :id_first_partner and m.id_second_partner = :id_second_partner) or
                     (m.id_first_partner = :id_second_partner and m.id_second_partner = :id_first_partner)) 
                     and c1.is_like is true
                     and c2.is_like is true
            """,
            values={
                "id_first_partner": int(userId),
                "id_second_partner": int(newPartner),
            },
        )
        if bool(len([list(result.values()) for result in results])):
            return False
        return True

    async def insertMeet(
        self, idUser: int, findPartnerId: int, algothmTime: datetime
    ) -> None:
        await self.database.execute(
            """
        INSERT INTO meets (
                id
                ,id_first_partner
                ,id_second_partner
                ,datetime_algorithm
        ) VALUES (
                :id
                ,:id_first_partner
                ,:id_second_partner
                ,:datetime_algorithm
            )
        """,
            values={
                "id": uuid.uuid1(),
                "id_first_partner": idUser,
                "id_second_partner": findPartnerId,
                "datetime_algorithm": algothmTime,
            },
        )


    async def getIdMeetLastMeet(self, idUser: str):
        columns = ["ids"]
        df = await self.get_df(f"""
            SELECT id 
            FROM meets 
            WHERE 1=1
                  and (id_first_partner = {int(idUser)} or id_second_partner = {int(idUser)})
                  and date_algorithm = (select max(date_algorithm) from meets)
            """, columns=columns)
        return df.ids.values[0]

    
    async def insertComment(self, data:  dict) -> None:
        await self.database.execute(
            """INSERT INTO comments (
                id
                ,id_registration
                ,id_meet
                ,is_find_partner
                ,find_partner
                ,is_like
                ,why
            ) VALUES (
                 :id
                ,:id_registration
                ,:id_meet
                ,:is_find_partner
                ,:find_partner
                ,:is_like
                ,:why
            )
        """,
            values={
                "id": data["id"],
                "id_registration": data["id_registration"],
                "id_meet": data["id_meet"],
                "is_find_partner": data["is_find_partner"],
                "find_partner": data["find_partner"],
                "is_like": data["is_like"],
                "why": data["why"],
            },
        )