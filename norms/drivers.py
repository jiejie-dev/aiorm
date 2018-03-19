import asyncio

import aiomysql

from norms.connections.connections import IConnection
from norms.connections.mysql_connection import MysqlConnection
from norms.query.query_compiler import MysqlQueryCompiler


class DataBaseDriver(object):
    async def initialize(self, loop: asyncio.AbstractEventLoop, configs):
        raise NotImplementedError()

    async def get_connection(self) -> IConnection:
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()


class MysqlDataBaseDriver(DataBaseDriver):
    async def initialize(self, loop: asyncio.AbstractEventLoop, configs: dict):
        kw = configs
        self.__pool = await aiomysql.create_pool(
            host=kw.get('host', 'localhost'),
            port=kw.get('port', 3306),
            user=kw['user'],
            password=kw['password'],
            db=kw['name'],
            charset=kw.get('charset', 'utf8'),
            autocommit=kw.get('autocommit', True),
            maxsize=kw.get('pool_maxsize', 10),
            minsize=kw.get('pool_minsize', 1),
            loop=loop
        )

    async def get_connection(self) -> IConnection:
        _conn = await self.__pool.acquire()
        return MysqlConnection(_conn, compiler=MysqlQueryCompiler())

    @property
    def name(self):
        return 'MYSQL'


class DriverManager(object):

    def __init__(self):
        self.drivers = {}

    def get_driver(self, name):
        return self.drivers[name]

    def register(self, name, driver):
        self.drivers[name] = driver
