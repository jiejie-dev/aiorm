import mock

from norm.connections.connections import IConnection
from norm.drivers import MySQLDataBaseDriver, DriverManager
import pytest
from tests.configtest import configs


@pytest.fixture()
async def driver(event_loop):
    driver = MySQLDataBaseDriver()

    await driver.initialize(event_loop, configs['mysql'])
    return driver


@pytest.fixture()
async def connection(driver):
    return await driver.get_connection()


@pytest.mark.asyncio
async def test_get_connection(event_loop):
    driver = MySQLDataBaseDriver()

    await driver.initialize(event_loop, configs['mysql'])

    connection = await driver.get_connection()
    assert connection is not None
    assert isinstance(connection, IConnection)
    assert await connection.execute('SHOW TABLES', None) > 0


@pytest.mark.asyncio
async def test_fixture(driver, connection):
    assert isinstance(driver, MySQLDataBaseDriver)
    assert isinstance(connection, IConnection)


@pytest.mark.asyncio
async def test_driver_manager(event_loop):
    manager = DriverManager()
    manager.initialize(event_loop, configs)

    get_driver = manager.get_driver('mysql')
    assert isinstance(get_driver, MySQLDataBaseDriver)
