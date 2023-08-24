import aiosqlite


class DataBase:

    def __init__(self):
        self.db_name = "karma.db"

    async def get_data(self):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            query = 'SELECT * FROM users ORDER BY karma DESC LIMIT 50'
            await cursor.execute(query)
            return await cursor.fetchall()

    async def create_table(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS users(
                name TEXT,
                id INT,
                karma INT
            )"""
            await cursor.executescript(query)
            await db.commit()

    async def get_user(self, member):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            query = 'SELECT * FROM users WHERE id = ?'
            await cursor.execute(query, (member.id,))
            return await cursor.fetchone()

    async def insert_new_member(self, member):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute("SELECT id FROM users WHERE id = ?", [member.id])
            if await cursor.fetchone() is None:
                await cursor.execute("INSERT INTO users VALUES(?, ?, ?)", [member.display_name, member.id, 0])

            await db.commit()

    async def update_member(self, query, values: list):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(query, values)
            await db.commit()

    async def delete_member(self, member):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute("DELETE FROM users WHERE id = ?", [member.id])
            await db.commit()
