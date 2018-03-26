import asyncio
import importlib
import typing
from abc import abstractmethod, ABCMeta

import os


class DataBaseDriver(object, metaclass=ABCMeta):
    NAME = 'NONE'

    def __init__(self):
        self.pool = None

    @abstractmethod
    async def initialize(self, loop: asyncio.AbstractEventLoop, configs):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    @abstractmethod
    def connection(self) -> 'AbstractConnection':
        raise NotImplementedError()

    @staticmethod
    def get(configs: dict, name=None) -> 'DataBaseDriver':
        abs = os.path.dirname(__file__)
        files = os.listdir(abs)

        if not name:
            name = configs.get('default')

        if name not in files:
            raise FileNotFoundError(name)
        m = importlib.import_module('aiorm.backends.{name}.driver'.format(name=name))
        fns = dir(m)
        for fn in fns:
            if fn.lower().startswith(name.lower()) and fn.lower().endswith('driver'):
                return getattr(m, fn)()


class AbstractConnection(object, metaclass=ABCMeta):

    @abstractmethod
    async def connect(self):
        raise NotImplementedError()

    @abstractmethod
    async def transaction(self):
        raise NotImplementedError()

    @abstractmethod
    async def begin_transaction(self):
        raise NotImplementedError()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    async def execute(self, sql, args):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    @abstractmethod
    async def cursor(self, sql, args):
        raise NotImplementedError()


class AbstractDataSet(object, metaclass=ABCMeta):

    @abstractmethod
    async def fetch_one(self):
        raise NotImplementedError()

    @abstractmethod
    async def fetch_many(self, n):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    async def __anext__(self):
        one = await self.fetch_one()
        if not one:
            raise StopAsyncIteration
        return one

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False


class QueryCompiler(object):
    maker = '?'

    def compile(self, query) -> typing.Tuple[str, list]:
        NotImplementedError()

    def raw_sql(self, query) -> str:
        if isinstance(query, str):
            return query

        sql = self.compile(query)
        for item in query._args:
            sql = sql.replace(self.maker, item, 1)
        return sql

    @staticmethod
    def get(name) -> 'QueryCompiler':
        abs = os.path.dirname(__file__)
        files = os.listdir(abs)

        if name not in files:
            raise FileNotFoundError(name)
        m = importlib.import_module('aiorm.backends.{name}.compiler'.format(name=name))
        fns = dir(m)
        for fn in fns:
            if fn.lower().startswith(name.lower()) and fn.lower().endswith('compiler'):
                return getattr(m, fn)()
