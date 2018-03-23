import pytest

from aiorm.backends.mysql.driver import MySQLDataBaseDriver
from aiorm.orm.connections import Connection
from aiorm.orm.contexts import Demo


@pytest.mark.asyncio
async def test_insert(connection: Connection):
    data = Demo()
    r = await connection.insert(data)
    assert r == 1


@pytest.mark.asyncio
async def test_insert(driver: MySQLDataBaseDriver):
    db = await driver.connection()
    db.insert(Demo())
