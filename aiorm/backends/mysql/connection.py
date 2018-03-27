import logging

import aiomysql
from aiocontext import async_contextmanager

from aiorm.backends.base import AbstractConnection, DataBaseDriver
from aiorm.backends.mysql.dataset import MySQLDataSet
from aiorm.orm.errors import AiormDbError

logger = logging.getLogger('aiorm')
logger.setLevel(logging.DEBUG)


class MySQLConnection(AbstractConnection):
    def __init__(self, driver: DataBaseDriver):
        self.driver = driver
        self._connection = None  # type: aiomysql.Connection
        self._transactions = 0

    async def connect(self):
        self._connection = await self.driver.pool.acquire()  # type: aiomysql.Connection
        await self._connection.begin()

    async def close(self):
        self._connection.close()

    @async_contextmanager
    async def transaction(self):
        await self.begin_transaction()

        try:
            yield self
        except Exception as e:
            await self.rollback()
            raise

        try:
            await self.commit()
        except Exception:
            await self.rollback()
            raise

    async def begin_transaction(self):
        self._transactions += 1
        self._connection.autocommit(False)

    async def commit(self):
        if self._transactions == 1:
            self._connection.commit()

        self._transactions -= 1

    async def rollback(self):
        if self._transactions == 1:
            self._transactions = 0

            await self._connection.rollback()
        else:
            self._transactions -= 1

    def transaction_level(self):
        return self._transactions

    async def execute(self, sql, args=None):
        logger.debug('{} {}'.format(sql, args))

        cursor = await self._connection.cursor(aiomysql.DictCursor)
        try:
            res = await cursor.execute(sql, args)
        except:
            raise AiormDbError('{} {}'.format(sql, args))
        finally:
            await cursor.close()
        return res

    async def cursor(self, sql, args):
        logger.debug('{} {}'.format(sql, args))
        try:
            cursor = await self._connection.cursor(aiomysql.DictCursor)
            await cursor.execute(sql, args)
            return MySQLDataSet(cursor)
        except:
            raise AiormDbError('{} {}'.format(sql, args))
