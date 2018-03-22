import asyncio

import aiomysql

from norm.connections.connections import IConnection
from norm.connections.mysql_connection import MySQLConnection
from norm.query.query_compiler import MySQLQueryCompiler


class DataBaseDriver(object):
    async def initialize(self, loop: asyncio.AbstractEventLoop, configs):
        raise NotImplementedError()

    async def get_connection(self) -> IConnection:
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()


class MySQLDataBaseDriver(DataBaseDriver):
    """ A database driver represent a home to store connection pool and provider connection"""
    NAME = 'MYSQL'

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
        return MySQLConnection(_conn, compiler=MySQLQueryCompiler())


class DataBaseEngine(object):
    """ Manage database drivers"""

    def __init__(self):
        self.drivers = {}

        self.drivers[MySQLDataBaseDriver.NAME.lower()] = MySQLDataBaseDriver

    def initialize(self, loop, configs: dict):
        self.loop = loop
        self.configs = configs

    def get_driver(self, name=None) -> DataBaseDriver:
        if not name:
            name = self.configs['default']
        driver_class = self.drivers[name]
        driver = driver_class()
        db_config = self.configs[name]
        driver.initialize(self.loop, db_config)
        return driver

    def register_driver(self, name, driver):
        self.drivers[name] = driver
