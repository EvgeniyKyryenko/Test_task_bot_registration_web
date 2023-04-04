import aiosqlite
from sqlite3 import Error
from models import UserInfoTG

DATABASE_NAME = 'tg_reg.db'


class Database:
    @staticmethod
    async def ConnectDB(**kwargs):
        try:
            conn = await aiosqlite.connect(DATABASE_NAME)
            cur = await conn.cursor()
            await cur.execute(
                "CREATE TABLE IF NOT EXISTS UserInfoTG (id, email, password, tg_id, first_name, last_name, username, bio, photo)")
            await conn.commit()
            return conn
        except Error:
            print(Error)

    @staticmethod
    async def write_to_db(conn, User: UserInfoTG):
        cur = await conn.cursor()
        await cur.execute(
            "INSERT INTO UserInfoTG(id,email,password,tg_id,first_name,last_name,username,bio,photo) VALUES (?,?,?,?,?,?,?,?,?)",
            (str(User.id), User.email, User.password, User.tg_id, User.first_name, User.last_name, User.username, User.bio,User.photo))
        await conn.commit()
        await conn.close()

    @staticmethod
    async def read_db(conn):
        conn.row_factory = aiosqlite.Row
        cur = await conn.cursor()
        await cur.execute("SELECT * FROM UserInfoTG")
        rows = await cur.fetchall()
        data = [dict(row) for row in rows]
        await conn.close()
        return data
