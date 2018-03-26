import aiomysql

from aiorm.backends.base import AbstractDataSet


class MySQLDataSet(AbstractDataSet):

    def __init__(self, cursor: aiomysql.DictCursor):
        self.cursor = cursor

    async def fetch_one(self):
        return self.cursor.fetchone()

    async def fetch_many(self, n):
        return self.cursor.fetchmany(n)

    async def fetch_all(self):
        return self.cursor.fetchall()
