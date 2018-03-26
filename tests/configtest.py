import functools
import sqlparse
import pytest
from sample.models import configs
from aiorm.backends.mysql.driver import MySQLDataBaseDriver

_format_sql = functools.partial(sqlparse.format, reindent=True)


def format_sql(sql):
    return _format_sql(sql.lower())


@pytest.fixture()
async def driver(event_loop):
    driver = MySQLDataBaseDriver()
    await driver.initialize(event_loop, configs['mysql'])
    return driver
