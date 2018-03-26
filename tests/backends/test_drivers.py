import pytest

from aiorm.backends.base import DataBaseDriver
from aiorm.backends.mysql.driver import MySQLDataBaseDriver
from sample.models import configs


@pytest.fixture()
async def driver(event_loop):
    driver = MySQLDataBaseDriver()

    await driver.initialize(event_loop, configs['mysql'])
    return driver


def test_get_driver():
    driver = DataBaseDriver.get(configs)
    assert isinstance(driver, DataBaseDriver)
    driver = DataBaseDriver.get(configs, name='mysql')
    assert isinstance(driver, DataBaseDriver)
