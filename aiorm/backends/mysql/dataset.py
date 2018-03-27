import aiomysql

from aiorm.backends.base import AbstractDataSet


class MySQLDataSet(AbstractDataSet):

    def __init__(self, cursor: aiomysql.DictCursor):
        self.cursor = cursor

    async def fetch_one(self):
        return await self.cursor.fetchone()

    async def fetch_many(self, n):
        return await self.cursor.fetchmany(n)

    async def fetch_all(self):
        return await self.cursor.fetchall()

    async def close(self):
        await self.cursor.close()