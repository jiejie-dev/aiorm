import logging
from contextlib import contextmanager
from logging import Logger

import aiomysql

from norm.query.query_base import Query
from norm.query.query_compiler import QueryCompiler
from aiocontext import async_contextmanager


class IConnection(object):

    async def select_one(self, query):
        raise NotImplementedError()

    async def select(self, query):
        raise NotImplementedError()

    async def insert(self, query):
        raise NotImplementedError()

    async def update(self, query):
        raise NotImplementedError()

    async def delete(self, query):
        raise NotImplementedError()

    async def transaction(self):
        raise NotImplementedError()

    async def begin_transaction(self):
        raise NotImplementedError()

    async def commit(self):
        raise NotImplementedError()

    async def rollback(self):
        raise NotImplementedError()

    async def execute(self, sql, args):
        raise NotImplementedError()


class Connection(IConnection):
    def __init__(self, conn, compiler: QueryCompiler = None, logger: Logger = None):
        self._connection = conn
        self.compiler = compiler

        self.logger = logger if logger is not None else logging.getLogger('norm')
        self.logger.setLevel(logging.DEBUG)

        self._transactions = 0

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

    async def new_cursor(self):
        pass

    async def execute(self, sql, args=None):
        cursor = await self.new_cursor()
        # self.logger.debug(sql, args)
        await cursor.execute(sql, args)
        # affected = cursor.rowcount
        # await cursor.close()
        # return affected

    async def insert(self, query_or_data):

        if not isinstance(query_or_data, Query):
            query = Query(None).insert(query_or_data)
        else:
            query = query_or_data

        exe_query, args = self.compiler.compile(query)

        cursor = await self.new_cursor()

        # self.logger.debug(self.compiler.raw_sql(query))

        await cursor.execute(exe_query, args)

        # affected = cursor.rowcount
        # await cursor.close()
        # return affected

    async def select(self, query):
        if isinstance(query, Query):
            exe_query, args = self.compiler.compile(query)
        else:
            exe_query, args = query, None

        cursor = await self.new_cursor()

        self.logger.debug(self.compiler.raw_sql(exe_query), args)

        await cursor.execute(exe_query, args)
        rs = await cursor.fetchall()
        await cursor.close()
        return rs

    async def update(self, query):
        exe_query, args = self.compiler.compile(query)
        await self.execute(exe_query, args)

    async def delete(self, query):
        exe_query, args = self.compiler.compile(query)
        await self.execute(exe_query, args)
