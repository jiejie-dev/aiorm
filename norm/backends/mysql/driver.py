import aiomysql
import asyncio

from norm.backends.base import DataBaseDriver
from norm.backends.mysql.compiler import MySQLQueryCompiler
from norm.orm.connections import AbstractConnection, Connection


class MySQLDataBaseDriver(DataBaseDriver):
    """ A database driver represent a home to store connection pool and provider connection"""
    NAME = 'mysql'

    async def initialize(self, loop: asyncio.AbstractEventLoop, configs: dict):
        kw = configs
        self.pool = await aiomysql.create_pool(
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
        )  # type: aiomysql.Pool

    async def connection(self) -> Connection:
        _conn = await self.pool.acquire()
        await _conn.begin()
        return Connection(_conn, compiler=MySQLQueryCompiler())
