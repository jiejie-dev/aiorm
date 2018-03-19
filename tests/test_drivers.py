from norms.connections.connections import IConnection
from norms.drivers import MysqlDataBaseDriver
import pytest
from tests.base import configs


@pytest.fixture()
async def driver(event_loop):
    driver = MysqlDataBaseDriver()

    await driver.initialize(event_loop, configs)
    return driver


@pytest.fixture()
async def connection(driver):
    return await driver.get_connection()


@pytest.mark.asyncio
async def test_get_connection(event_loop):
    driver = MysqlDataBaseDriver()

    await driver.initialize(event_loop, configs)

    connection = await driver.get_connection()
    assert connection is not None
    assert isinstance(connection, IConnection)
    assert await connection.execute('SHOW TABLES', None) > 0


@pytest.mark.asyncio
async def test_fixture(driver, connection):
    assert isinstance(driver, MysqlDataBaseDriver)
    assert isinstance(connection, IConnection)
