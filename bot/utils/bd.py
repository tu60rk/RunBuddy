import pandas as pd
import uuid

from datetime import datetime
from typing import List, Union
# from databases import Database

from settings.config import botMainDbSettings, botMainSettings


admins = [int(i) for i in botMainSettings.ADMINS.split(",")]

class NotSelectInSql(Exception):
    pass


class NotInsertInSql(Exception):
    pass


# class DataBase:
#     database = Database(botMainDbSettings.dsl_database)

#     async def getRegisteredUsers(self) -> pd.DataFrame:
#         columns = [
#             "id",
#             "name",
#             "lastName",
#             "nickName",
#             "age",
#             "sex",
#             "city",
#             "runLevel",
#             "accountLink",
#             "levelPartnerNeed",
#             "anyGender",
#             "meetActive",
#             "idTelegram",
#             "phoneNumber",
#             "linkTelegram",
#             "active"
#         ]
#         df = await self.get_df(
#             f"""SELECT 
#             id
#             ,name
#             ,last_name
#             ,nick_name
#             ,age
#             ,sex
#             ,city
#             ,run_level
#             ,account_link
#             ,level_partner_need
#             ,any_gender
#             ,meet_active
#             ,id_telegram
#             ,phone_number
#             ,link_telegram
#             ,active
#          FROM registration
#         """,
#             columns=columns,
#         )
#         return df

#     async def getActiveUsers(self) -> pd.DataFrame:
#         columns = [
#             "id",
#             "name",
#             "lastName",
#             "nickName",
#             "age",
#             "sex",
#             "city",
#             "runLevel",
#             "accountLink",
#             "levelPartnerNeed",
#             "anyGender",
#             "meetActive",
#             "idTelegram",
#             "phoneNumber",
#             "linkTelegram",
#             "active"
#         ]
#         df = await self.get_df(
#             f"""SELECT 
#             id
#             ,name
#             ,last_name
#             ,nick_name
#             ,age
#             ,sex
#             ,city
#             ,run_level
#             ,account_link
#             ,level_partner_need
#             ,any_gender
#             ,meet_active
#             ,id_telegram
#             ,phone_number
#             ,link_telegram
#             ,active
#          FROM registration WHERE meet_active is true""",
#             columns=columns,
#         )
#         return df

#     async def getUserRegistrationId(self, idTelegram: int):
#         columns = ["ids"]
#         df = await self.get_df(
#             f"SELECT id FROM registration WHERE id_telegram = '{idTelegram}'",
#             columns=columns,
#         )
#         return df.ids.values[0]

#     async def getMeets(self) -> pd.DataFrame:
#         columns = [
#             "id",
#             "nickNameUserOne",
#             "nickNameUserTwo",
#             "algorithmDate",
#             "userOneAnswer",
#             "userTwoAnswer",
#         ]
#         return await self.get_df(
#             """SELECT 
#                 m.id
#                 , r1.nick_name
#                 , r2.nick_name
#                 , m.date_algorithm
#                 , m.first_partner_meet
#                 , m.second_partner_meet
#             FROM meets m left join registration r1 on m.id_first_partner = r1.id
#                          left join registration r2 on m.id_second_partner = r2.id
#             """,
#             columns=columns,
#         )

#     async def getComments(self) -> pd.DataFrame:
#         columns = [
#             "id",
#             "nickname",
#             "telephone",
#             "dateComment",
#             "comment",
#         ]
#         return await self.get_df(
#             """SELECT 
#                 cm.id
#                 , r.nick_name
#                 , r.phone_number
#                 , cm.date_comment
#                 , cm.comment
#             FROM comments cm left join registration r on cm.id_telegram = r.id_telegram
#             """,
#             columns=columns,
#         )

#     async def insertCommonComment(
#         self, id_telegram: str, comment: str,
#     ) -> None:
#         await self.database.execute(
#             """
#         INSERT INTO comments (
#                 id
#                 ,id_telegram
#                 ,date_comment
#                 ,comment
#         ) VALUES (
#                 :id
#                 ,:id_telegram
#                 ,:date_comment
#                 ,:comment
#             )
#         """,
#             values={
#                 "id": uuid.uuid1(),
#                 "id_telegram": id_telegram,
#                 "date_comment": datetime.now().date(),
#                 "comment": comment,
#             },
#         )

#     async def isCanGetComment(self, userId) -> bool:
#         results = await self.database.fetch_all(
#             f"""
#             select id from meets m 
#             where 
#                 m.id_first_partner in (SELECT id FROM registration WHERE id_telegram = '{userId}') or 
#                 m.id_second_partner in (SELECT id FROM registration WHERE id_telegram = '{userId}')
#             """,
#         )
#         return bool(len([list(result.values()) for result in results]))
    
#     async def getMeetById(self, meetId: str) -> pd.DataFrame:
#         columns = [
#             "id",
#             "idUserOne",
#             "idUserTwo",
#             "algorithmDate",
#             "userOneAnswer",
#             "userTwoAnswer",
#         ]
#         return await self.get_df(
#             f"SELECT * FROM meets WHERE id = '{meetId}'",
#             columns=columns,
#         )

#     async def whichUserInMeet(self, meetId: str, userId: str) -> pd.DataFrame:
#         df = await self.getMeetById(meetId=meetId)
#         if not df[df.idUserOne == userId].empty:
#             return 1
#         return 2

#     async def getMeetStatus(self, userId: int) -> list:
#         results = await self.database.fetch_all(
#             f"SELECT meet_active FROM registration WHERE id_telegram = '{userId}'"
#         )
#         return [list(result.values()) for result in results]

#     async def deleteRegistrationDataByUser(self, userId: int) -> None:
#         await self.database.execute(
#             f"DELETE FROM registration WHERE id_telegram = '{userId}'",
#             # values={"id_telegram": int(userId)},
#         )

#     async def addRegistrationData(self, data: dict) -> None:
#         await self.database.execute(
#             """INSERT INTO registration (
#                 id
#                 ,name
#                 ,last_name
#                 ,nick_name
#                 ,age
#                 ,sex
#                 ,city
#                 ,run_level
#                 ,account_link
#                 ,level_partner_need
#                 ,any_gender
#                 ,meet_active
#                 ,phone_number
#                 ,id_telegram
#                 ,link_telegram
#                 ,active
#             ) VALUES (
#                  :id
#                 ,:name
#                 ,:last_name
#                 ,:nick_name
#                 ,:age
#                 ,:sex
#                 ,:city
#                 ,:run_level
#                 ,:account_link
#                 ,:level_partner_need
#                 ,:any_gender
#                 ,:meet_active
#                 ,:phone_number
#                 ,:id_telegram
#                 ,:link_telegram
#                 ,:active
#             )
#         """,
#             values={
#                 "id": data["id"],
#                 "name": data["name"],
#                 "last_name": data["last_name"],
#                 "nick_name": data["nick_name"],
#                 "age": data["age"],
#                 "sex": data["sex"],
#                 "city": data["city"],
#                 "run_level": data["run_level"],
#                 "account_link": data["account_link"],
#                 "level_partner_need": data["level_partner_need"],
#                 "any_gender": data["any_gender"],
#                 "meet_active": data["meet_active"],
#                 "phone_number": str(data["phone_number"]),
#                 "id_telegram": str(data["id_telegram"]),
#                 "link_telegram": data["link_telegram"],
#                 "active": data["active"],
#             },
#         )

#     async def updateRegistrationData(
#         self, userId: int, columnName: str, data: str
#     ) -> None:
#         await self.database.execute(
#             f"""
#             UPDATE registration SET {columnName} = :column_name
#             WHERE id_telegram = '{userId}'
#         """,
#             values={"column_name": data},
#         )

#     def isAdmin(self, userId: str) -> bool:
#         if int(userId) in admins:
#             return True
#         return False

#     async def isRegistration(self, userId: int) -> bool:
#         results = await self.database.fetch_all(
#             f"SELECT * FROM registration WHERE id_telegram = '{userId}'",
#             # values={"user_id": userId},
#         )
#         return bool(len([list(result.values()) for result in results]))

#     async def isNewPartner(self, userId: str, newPartner: str) -> bool:
#         results = await self.database.fetch_all(
#             f"""  
#                SELECT m.id 
#                FROM meets m 
#                WHERE ((m.id_first_partner = '{userId}'::uuid and m.id_second_partner = '{newPartner}'::uuid) or
#                      (m.id_first_partner = '{newPartner}'::uuid and m.id_second_partner = '{userId}'::uuid))
#             """,
#             # values={
#             #     "id_first_partner": userId,
#             #     "id_second_partner": newPartner,
#             # },
#         )
#         if bool(len([list(result.values()) for result in results])):
#             return False
#         return True

#     async def isNewPartnerForPartnerAlgorithm(
#         self, userId: str, newPartner: str
#     ) -> bool:
#         results = await self.database.fetch_all(
#             f"""SELECT m.id 
#                FROM meets m 
#                LEFT JOIN comments c1 on m.id = c1.id_meet and m.id_first_partner = c1.id_registration
#                LEFT JOIN comments c2 on m.id = c2.id_meet and m.id_second_partner = c2.id_registration
#                id_registration id_partner
#                WHERE ((m.id_first_partner = '{userId}'::uuid and m.id_second_partner = '{newPartner}'::uuid) or
#                      (m.id_first_partner = '{newPartner}'::uuid and m.id_second_partner = '{userId}'::uuid)) 
#                      and c1.is_like is true
#                      and c2.is_like is true
#             """,
#             # values={
#             #     "id_first_partner": int(userId),
#             #     "id_second_partner": int(newPartner),
#             # },
#         )
#         if bool(len([list(result.values()) for result in results])):
#             return False
#         return True

#     async def insertMeet(
#         self, idUser: int, findPartnerId: int, algothmTime: datetime,
#     ) -> None:
#         await self.database.execute(
#             """
#         INSERT INTO meets (
#                 id
#                 ,id_first_partner
#                 ,id_second_partner
#                 ,date_algorithm
#         ) VALUES (
#                 :id
#                 ,:id_first_partner
#                 ,:id_second_partner
#                 ,:date_algorithm
#             )
#         """,
#             values={
#                 "id": uuid.uuid1(),
#                 "id_first_partner": idUser,
#                 "id_second_partner": findPartnerId,
#                 "date_algorithm": algothmTime,
#                 # "status": status
#             },
#         )

#     async def getIdMeetLastMeet(self, idUser: str):
#         columns = ["ids"]
#         df = await self.get_df(
#             f"""
#             SELECT id 
#             FROM meets 
#             WHERE 1=1
#                   and (id_first_partner = '{idUser}'::uuid or id_second_partner = '{idUser}'::uuid)
#                   and date_algorithm = (select max(date_algorithm) from meets)
#             """,
#             columns=columns,
#         )
#         try:
#             return df.ids.values[0]
#         except:
#             return ""
    
#     async def getLastMeet(self):
#         columns = ["ids"]
#         df = await self.get_df(
#             f"""
#             with test as (
#                 select max(date_algorithm) as mx_date from meets
#             ),
#             test1 as (
#                 SELECT r.id_telegram
#                 FROM meets m 
#                     inner join registration r on m.id_first_partner = r.id
#                     inner join test t on m.date_algorithm = t.mx_date
                
#                 union all
#                 SELECT r.id_telegram as ids 
#                 FROM meets m 
#                     inner join registration r on m.id_second_partner = r.id
#                     inner join test t on m.date_algorithm = t.mx_date
#             )
#             select distinct id_telegram from test1
#             """,
#             columns=columns,
#         )
#         return df.ids.values.tolist()
    
#     async def getMaxDateMeet(self) -> list:
#         columns = ["maxDate"]
#         df = await self.get_df(
#             "select max(date_algorithm) from meets",
#             columns=columns,
#         )
#         return df.maxDate.values[0]

#     async def updateMeetData(
#         self, meetId: str, columnName: str, data: str
#     ) -> None:
#         await self.database.execute(
#             f"""
#             UPDATE meets SET {columnName} = :data
#             WHERE id = :meet_id
#         """,
#             values={"data": data, "meet_id": meetId},
#         )

#     async def insertComment(self, data: dict) -> None:
#         await self.database.execute(
#             """INSERT INTO comments (
#                 id
#                 ,id_registration
#                 ,id_meet
#                 ,is_find_partner
#                 ,find_partner
#                 ,is_like
#                 ,why
#                 ,create_by_system
#             ) VALUES (
#                  :id
#                 ,:id_registration
#                 ,:id_meet
#                 ,:is_find_partner
#                 ,:find_partner
#                 ,:is_like
#                 ,:why
#                 ,:create_by_system
#             )
#         """,
#             values={
#                 "id": data["id"],
#                 "id_registration": data["id_registration"],
#                 "id_meet": data["id_meet"],
#                 "is_find_partner": data["is_find_partner"],
#                 "find_partner": data["find_partner"],
#                 "is_like": data["is_like"],
#                 "why": data["why"],
#                 "create_by_system": data["create_by_system"],
#             },
#         )

#     async def commentExist(self, idUser: str, idMeet: str) -> bool:
#         results = await self.database.fetch_all(
#             f"SELECT id FROM comments WHERE id_registration = '{idUser}'::uuid and id_meet = '{idMeet}'::uuid",
#             # values={"id_registration": idUser, "id_meet": idMeet},
#         )
#         return bool(len([list(result.values()) for result in results]))

#     async def getUsersWhichDontAnswer(self) -> str:
#         columns = ["ids", "nickName", "summed"]
#         df = await self.get_df(
#             sql="""with last_dates as (

#                 SELECT date_algorithm 
#                 FROM meets
#                 ORDER BY date_algorithm DESC
#                 LIMIT 3

#                 ),
                
#                 un as (
#                 select 
#                     m1.id_first_partner as id, 
#                     m1.first_partner_meet as meeted 
#                 FROM meets m1 
#                     join last_dates ld1 on m1.date_algorithm = ld1.date_algorithm
#                 union all
#                 select 
#                     m2.id_second_partner as id, 
#                     m2.second_partner_meet as meeted 
#                 FROM meets m2 
#                     join last_dates ld1 on m2.date_algorithm = ld1.date_algorithm
#                 )
#                 select 
#                     un.id,
#                     r.nick_name, 
#                     sum(case when meeted is not false then 0 else 1 end) as sm
#                 from un left join registration r on un.id = r.id
#                 group by un.id, r.nick_name
#                 having sum(case when meeted is not false then 0 else 1 end) >= 3;""",
#             columns=columns,
#         )

#         text = ""
#         if not df.empty:
#             text += "Следующие пользователи не смогли договориться о встречи 3 недели подряд: \n"
#             for index, row in df.iterrows():
#                 text += f"{row[1]}\n"
#         return text

#     async def get_df(self, sql: str, columns: list) -> pd.DataFrame:
#         if "select" in sql.lower():
#             results = await self.database.fetch_all(sql)
#             new_df = [list(result.values()) for result in results]
#             df = pd.DataFrame(new_df, columns=columns)
#             return df
#         raise NotSelectInSql("Not select in sql!")
    
#     async def setActive(self, user_id: str, active: bool) -> None:
#         await self.database.execute(
#             "UPDATE registration SET active = :active WHERE id_telegram = :user_id",
#             values={"active": active, "user_id": user_id},
#         )
    
#     async def getUsers(self) -> List[Union[str, int]]:
#         results = await self.database.fetch_all("SELECT id_telegram, active FROM registration")
#         return [list(result.values()) for result in results]

class DataBase:
    async def getRegisteredUsers(self):
        pass

    async def getActiveUsers(self):
        pass

    async def getUserRegistrationId(self, idTelegram: int):
        pass

    async def getMeets(self) -> pd.DataFrame:
        pass
    async def getComments(self) -> pd.DataFrame:
        pass
    async def insertCommonComment(
        self, id_telegram: str, comment: str,
    ) -> None:
        pass
    async def isCanGetComment(self, userId) -> bool:
        pass  
    async def getMeetById(self, meetId: str) -> pd.DataFrame:
        pass
    async def whichUserInMeet(self, meetId: str, userId: str) -> pd.DataFrame:
        pass
    async def getMeetStatus(self, userId: int) -> list:
        pass
    async def deleteRegistrationDataByUser(self, userId: int) -> None:
        pass
    async def addRegistrationData(self, data: dict) -> None:
        pass
    async def updateRegistrationData(
        self, userId: int, columnName: str, data: str
    ) -> None:
        pass
    def isAdmin(self, userId: str) -> bool:
        pass
    async def isRegistration(self, userId: int) -> bool:
        pass
    async def isNewPartner(self, userId: str, newPartner: str) -> bool:
        pass
    async def isNewPartnerForPartnerAlgorithm(
        self, userId: str, newPartner: str
    ) -> bool:
        pass
    async def insertMeet(
        self, idUser: int, findPartnerId: int, algothmTime: datetime,
    ) -> None:
        pass
    async def getIdMeetLastMeet(self, idUser: str):
        pass   
    async def getLastMeet(self):
        pass    
    async def getMaxDateMeet(self) -> list:
        pass
    async def updateMeetData(
        self, meetId: str, columnName: str, data: str
    ) -> None:
        pass
    async def insertComment(self, data: dict) -> None:
        pass
    async def commentExist(self, idUser: str, idMeet: str) -> bool:
        pass
    async def getUsersWhichDontAnswer(self) -> str:
        pass
    async def get_df(self, sql: str, columns: list) -> pd.DataFrame:
        pass   
    async def setActive(self, user_id: str, active: bool) -> None:
        pass  
    async def getUsers(self) -> List[Union[str, int]]:
        pass

