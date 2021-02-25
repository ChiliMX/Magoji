from asyncpg import create_pool
from os import getenv


class Database:
    """A database interface for the bot to connect to Postgres."""

    def __init__(self):
        self.guilds = {}

    async def setup(self):
        self.pool = await create_pool(
            host=getenv("DB_HOST", "127.0.0.1"),
            port=getenv("DB_PORT", 5432),
            database=getenv("DB_DATABASE", "magoji"),
            user=getenv("DB_USER", "root"),
            password=getenv("DB_PASS", "password"),
        )

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def create_guild(self, id: int, prefix: str = ">"):
        await self.execute("INSERT INTO Guilds (id, prefix) VALUES ($1, $2);", id, prefix)

    async def fetch_guild(self, id: int):
        if id in self.guilds:
            return self.guilds[id]

        data = await self.fetchrow("SELECT * FROM Guilds WHERE id = $1;", id)
        self.guilds[id] = data
        return data
