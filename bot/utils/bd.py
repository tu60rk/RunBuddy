import pandas as pd
import os
import uuid

from datetime import datetime
from typing import List, Union
from databases import Database


DB_URL = os.getenv("DATABASE_URL")
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

    async def getUserRegistrationId(self, idTelegram: int):
        columns = ["ids"]
        df = await self.get_df(
            f"SELECT id FROM registration WHERE id_telegram = '{idTelegram}'",
            columns=columns,
        )
        return df.ids.values[0]

    async def getMeetStatus(self, userId: int) -> list:
        results = await self.database.fetch_all(
            f"SELECT meet_active FROM registration WHERE id_telegram = '{userId}'"
        )
        return [list(result.values()) for result in results]

    async def deleteRegistrationDataByUser(self, userId: int) -> None:
        await self.database.execute(
            f"DELETE FROM registration WHERE id_telegram = '{userId}'",
            # values={"id_telegram": int(userId)},
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
                "id_telegram": str(data["id_telegram"]),
                "link_telegram": data["link_telegram"],
            },
        )

    async def updateRegistrationData(
        self, userId: int, columnName: str, data: str
    ) -> None:
        await self.database.execute(
            f"""
            UPDATE registration SET {columnName} = :column_name
            WHERE id_telegram = '{userId}'
        """,
            values={"column_name": data},
        )

    def isAdmin(self, userId: str) -> bool:
        if int(userId) in admins:
            return True
        return False

    async def isRegistration(self, userId: int) -> bool:
        results = await self.database.fetch_all(
            f"SELECT * FROM registration WHERE id_telegram = '{userId}'",
            # values={"user_id": userId},
        )
        return bool(len([list(result.values()) for result in results]))

    async def isNewPartner(self, userId: str, newPartner: str) -> bool:
        results = await self.database.fetch_all(
            f"""
            with groupMeet as (
                select id_meet
                       ,max(case when find_partner is true then 1 else 0 end) as mxFindPartner 
                       ,min(case when find_partner is true then 1 else 0 end) as mnFindPartner
                from comments
                where id_registration in ('{userId}'::uuid, '{newPartner}'::uuid)
                group by id_meet
            )   
               SELECT m.id 
               FROM meets m LEFT JOIN groupMeet g on m.id = g.id_meet 
               WHERE ((m.id_first_partner = '{userId}'::uuid and m.id_second_partner = '{newPartner}'::uuid) or
                     (m.id_first_partner = '{newPartner}'::uuid and m.id_second_partner = '{userId}'::uuid)) 
                     and g.mxFindPartner = 1
                     and g.mnFindPartner = 1
            """,
            # values={
            #     "id_first_partner": userId,
            #     "id_second_partner": newPartner,
            # },
        )
        if bool(len([list(result.values()) for result in results])):
            return False
        return True

    async def isNewPartnerForPartnerAlgorithm(
        self, userId: str, newPartner: str
    ) -> bool:
        results = await self.database.fetch_all(
            f"""SELECT m.id 
               FROM meets m 
               LEFT JOIN comments c1 on m.id = c1.id_meet and m.id_first_partner = c1.id_registration
               LEFT JOIN comments c2 on m.id = c2.id_meet and m.id_second_partner = c2.id_registration
               id_registration id_partner
               WHERE ((m.id_first_partner = '{userId}'::uuid and m.id_second_partner = '{newPartner}'::uuid) or
                     (m.id_first_partner = '{newPartner}'::uuid and m.id_second_partner = '{userId}'::uuid)) 
                     and c1.is_like is true
                     and c2.is_like is true
            """,
            # values={
            #     "id_first_partner": int(userId),
            #     "id_second_partner": int(newPartner),
            # },
        )
        if bool(len([list(result.values()) for result in results])):
            return False
        return True

    async def insertMeet(
        self, idUser: int, findPartnerId: int, algothmTime: datetime,
    ) -> None:
        await self.database.execute(
            """
        INSERT INTO meets (
                id
                ,id_first_partner
                ,id_second_partner
                ,date_algorithm
        ) VALUES (
                :id
                ,:id_first_partner
                ,:id_second_partner
                ,:date_algorithm
            )
        """,
            values={
                "id": uuid.uuid1(),
                "id_first_partner": idUser,
                "id_second_partner": findPartnerId,
                "date_algorithm": algothmTime,
                # "status": status
            },
        )

    async def getIdMeetLastMeet(self, idUser: str):
        columns = ["ids"]
        df = await self.get_df(
            f"""
            SELECT id 
            FROM meets 
            WHERE 1=1
                  and (id_first_partner = '{idUser}'::uuid or id_second_partner = '{idUser}'::uuid)
                  and date_algorithm = (select max(date_algorithm) from meets)
            """,
            columns=columns,
        )
        try:
            return df.ids.values[0]
        except:
            return ""
    
    async def getLastMeet(self):
        columns = ["ids"]
        df = await self.get_df(
            f"""
            with test as (
                select max(date_algorithm) as mx_date from meets
            ),
            test1 as (
                SELECT r.id_telegram
                FROM meets m 
                    inner join registration r on m.id_first_partner = r.id
                    inner join test t on m.date_algorithm = t.mx_date
                
                union all
                SELECT r.id_telegram as ids 
                FROM meets m 
                    inner join registration r on m.id_second_partner = r.id
                    inner join test t on m.date_algorithm = t.mx_date
            )
            select distinct id_telegram from test1
            """,
            columns=columns,
        )
        return df.ids.values.tolist()
    
    async def getMaxDateMeet(self) -> list:
        columns = ["maxDate"]
        df = await self.get_df(
            "select max(date_algorithm) from meets",
            columns=columns,
        )
        return df.maxDate.values[0]

    async def updateMeetData(
        self, meetId: str, columnName: str, data: str
    ) -> None:
        await self.database.execute(
            f"""
            UPDATE meet SET {columnName} = :column_name
            WHERE id = :user_id
        """,
            values={"column_name": data, "meet_id": meetId},
        )

    async def insertComment(self, data: dict) -> None:
        await self.database.execute(
            """INSERT INTO comments (
                id
                ,id_registration
                ,id_meet
                ,is_find_partner
                ,find_partner
                ,is_like
                ,why
                ,create_by_system
            ) VALUES (
                 :id
                ,:id_registration
                ,:id_meet
                ,:is_find_partner
                ,:find_partner
                ,:is_like
                ,:why
                ,:create_by_system
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
                "create_by_system": data["create_by_system"],
            },
        )

    async def commentExist(self, idUser: str, idMeet: str) -> bool:
        results = await self.database.fetch_all(
            f"SELECT id FROM comments WHERE id_registration = '{idUser}'::uuid and id_meet = '{idMeet}'::uuid",
            # values={"id_registration": idUser, "id_meet": idMeet},
        )
        return bool(len([list(result.values()) for result in results]))

    async def get_df(self, sql: str, columns: list) -> pd.DataFrame:
        if "select" in sql.lower():
            results = await self.database.fetch_all(sql)
            new_df = [list(result.values()) for result in results]
            df = pd.DataFrame(new_df, columns=columns)
            return df
        raise NotSelectInSql("Not select in sql!")
