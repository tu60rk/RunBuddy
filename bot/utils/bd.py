import pandas as pd
import os
import logging

from typing import List, Union
from databases import Database
from sqlalchemy import column

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

DB_URL = os.getenv("DATABASE_URL")
ADMINS = os.getenv("ADMINS")
admins = [int(i) for i in ADMINS.split(",")]


class NotSelectInSql(Exception):
    pass


class NotInsertInSql(Exception):
    pass


class DataBase:
    database = Database(DB_URL)

    async def get_registration_data_by_user_id(self, userId: str) -> pd.DataFrame:
        columns = [
            "id",
            "name",
            "last_name",
            "age",
            "sex",
            "city",
            "run_level",
            "account_link",
            "level_partner_need",
            "any_gender",
            "meet_active",
            "id_telegram",
            "link_telegram",
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
            ,meet_active
            ,id_telegram
            ,link_telegram
         FROM registration WHERE id_telegram = {int(userId)}""",
            columns=columns,
        )
        return df

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

    async def isAdmin(self, userId: str) -> bool:
        if int(userId) in admins:
            return True
        return False

    async def isRegistration(self, userId: str) -> bool:
        results = await self.database.fetch_all(
            "SELECT * FROM registration WHERE id_telegram = :user_id",
            values={"user_id": int(userId)},
        )
        return bool(len([list(result.values()) for result in results]))

    # ------------------------------------------ #

    async def delete_pet(
        self, pet_name: str, telephone_number: int, chat_id: int
    ) -> None:
        await self.database.execute(
            f"""
            DELETE FROM my_pet
            WHERE chat_id = :chat_id
                  and pet_name = :pet_name
                  and telephone_number = :telephone_number
        """,
            values={
                "telephone_number": telephone_number,
                "chat_id": chat_id,
                "pet_name": pet_name,
            },
        )

    async def update_pet(
        self, user_id: str, pet_name: str, column_name: str, data: str
    ) -> None:
        await self.database.execute(
            f"""
            UPDATE my_pet SET {column_name} = :column_name
            WHERE chat_id = :user_id
                  and pet_name = :pet_name
        """,
            values={"column_name": data, "user_id": user_id, "pet_name": pet_name},
        )

    async def user_exists(self, user_id: str) -> bool:
        results = await self.database.fetch_all(
            "SELECT * FROM users WHERE user_id = :user_id", values={"user_id": user_id}
        )
        return bool(len([list(result.values()) for result in results]))

    async def add_user(self, user_id: str) -> None:
        max_id_user = await self.max_id_users()
        await self.database.execute(
            "INSERT INTO users (id, user_id, active) VALUES (:id, :user_id, :active)",
            values={"id": max_id_user + 1, "user_id": user_id, "active": 1},
        )

    async def set_active(self, user_id: str, active: int) -> None:
        await self.database.execute(
            "UPDATE users SET active = :active WHERE user_id = :user_id",
            values={"active": active, "user_id": user_id},
        )

    async def get_users(self) -> List[Union[str, int]]:
        results = await self.database.fetch_all("SELECT user_id, active FROM users")
        return [list(result.values()) for result in results]

    async def max_id_users(self) -> int:
        columns = ["ids"]
        df = await self.get_df(f"SELECT max(id) as ids  FROM users", columns=columns)
        return df.ids.values[0]

    async def get_df(self, sql: str, columns: list) -> pd.DataFrame:
        if "select" in sql.lower():
            results = await self.database.fetch_all(sql)
            new_df = [list(result.values()) for result in results]
            df = pd.DataFrame(new_df, columns=columns)
            return df
        raise NotSelectInSql("Not select in sql!")

    async def insert_any_data(self, sql: str, data: List[List]) -> None:
        if "insert" in sql.lower() and data:
            await self.database.execute_many(query=sql, values=data)
        else:
            raise NotInsertInSql('You try insert data without "Insert" in sql!')

    async def sql_execute(self, sql: str) -> None:
        await self.database.execute(sql)

    async def get_pet_names(self, telephone_number: int, chat_id: int) -> pd.DataFrame:
        columns = ["id", "pet_name"]
        return await self.get_df(
            f"SELECT id, pet_name FROM my_pet WHERE telephone_number = '{telephone_number}' and chat_id = {chat_id}",
            columns=columns,
        )

    async def get_pet_data(
        self, pet_name: str, telephone_number: int, chat_id: int
    ) -> pd.DataFrame:
        columns = [
            "id",
            "telephone_number",
            "chat_id",
            "pet_name",
            "pet_type",
            "pet_breed",
            "pet_birthday",
            "pet_gender",
            "pet_sterilized",
            "pet_vaccinated",
            "pet_last_date_vaccinated",
            "pet_chiped",
            "pet_number_chip",
            "last_clinic_name",
        ]
        return await self.get_df(
            f"SELECT * FROM my_pet WHERE telephone_number = '{telephone_number}' and chat_id = {chat_id} and pet_name = '{pet_name}'",
            columns=columns,
        )

    async def max_id_my_pet(self) -> int:
        columns = ["ids"]
        df = await self.get_df(
            f"SELECT max(id) as ids  FROM my_pet at_id", columns=columns
        )
        return df.ids.values[0]

    async def get_push_comment(self, type_comment: str) -> pd.DataFrame:
        columns = ["after_minute", "comment_text"]
        return await self.get_df(
            f"""
                    SELECT after_minute, comment_text
                    FROM push_setting 
                    WHERE id = (select max(id) from push_setting where type_comment = '{type_comment}')
                    """,
            columns,
        )

    async def max_id_push_comment(self) -> int:
        columns = ["ids"]
        df = await self.get_df(
            f"SELECT max(id) as ids  FROM push_setting", columns=columns
        )
        return df.ids.values[0]

    async def setting_time(self, type_comment: str) -> int:
        columns = ["after_minute"]
        df = await self.get_df(
            f"""SELECT after_minute 
                                   FROM push_setting 
                                   WHERE type_comment = '{type_comment}'
                                         and id = (SELECT max(id) as id 
                                                   FROM push_setting 
                                                   WHERE type_comment = '{type_comment}'
                                                )
                                """,
            columns=columns,
        )
        return int(df.after_minute.values[0])

    # requests for animals
    async def get_requests(self) -> pd.DataFrame:
        columns = [
            "req_id",
            "create_datetime",
            "user_id",
            "user_nik",
            "animal_type",
            "animal_gender",
            "animal_breed",
            "animal_age",
            "user_telephone",
        ]
        df = await self.get_df(f"SELECT * FROM requests", columns=columns)
        return df

    async def get_max_req_id(self) -> int:
        columns = ["ids"]
        df = await self.get_df(
            f"SELECT max(req_id) as ids  FROM requests", columns=columns
        )
        return df.ids.values[0]

    async def insert_requests(self, data: dict) -> None:

        logging.error(f"VALUES: {data}")
        await self.database.execute(
            """INSERT INTO requests (req_id , 
                                     create_datetime,
                                     user_id, 
                                     user_nik, 
                                     animal_type, 
                                     animal_gender, 
                                     animal_breed, 
                                     animal_age, 
                                     user_telephone
            ) VALUES (:req_id, :create_datetime, :user_id, :user_nik, :animal_type, :animal_gender, :animal_breed, :animal_age, :user_telephone)
        """,
            values={
                "req_id": int(data["req_id"]),
                "create_datetime": data["create_datetime"],
                "user_id": int(data["user_id"]),
                "user_nik": data["user_nik"],
                "animal_type": data["animal_type"],
                "animal_gender": data["animal_gender"],
                "animal_breed": data["animal_breed"],
                "animal_age": data["animal_age"],
                "user_telephone": data["user_telephone"],
            },
        )

    async def get_requests_statuses(self) -> pd.DataFrame:
        columns = [
            "req_id",
            "req_status",
            "req_datetime",
            "req_comment",
            "req_schedule_datetime",
        ]
        df = await self.get_df(f"SELECT * FROM requests_statuses", columns=columns)
        return df

    async def insert_requests_statuses(self, data: dict) -> None:
        await self.database.execute(
            """INSERT INTO requests_statuses (req_id , 
                                     req_status,
                                     req_datetime, 
                                     req_comment, 
                                     req_schedule_datetime
            ) VALUES (:req_id, :req_status, :req_datetime, :req_comment, :req_schedule_datetime)
        """,
            values={
                "req_id": data["req_id"],
                "req_status": data["req_status"],
                "req_datetime": data["req_datetime"],
                "req_comment": data["req_comment"],
                "req_schedule_datetime": data["req_schedule_datetime"],
            },
        )
