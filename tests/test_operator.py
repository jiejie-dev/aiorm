import uuid

import pytest
from aiomysql import create_pool

from norm.connections.connections import Connection
from norm.drivers import MySQLDataBaseDriver
from norm.query.query_base import Query
from norm.query.query_compiler import MySQLQueryCompiler
from tests.configtest import configs, Demo
from tests.test_drivers import connection, driver


@pytest.mark.asyncio
async def test_insert(connection: Connection):
    data = Demo()
    r = await connection.insert(data)
    assert r == 1

@pytest.mark.asyncio
async def test_insert(driver:MySQLDataBaseDriver):
    db = await driver.get_connection()
    db.insert(Demo())