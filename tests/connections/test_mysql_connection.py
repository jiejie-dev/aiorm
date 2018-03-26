import pytest
import mock

from aiorm.backends.base import AbstractConnection
from aiorm.backends.mysql.connection import MySQLConnection
from sample.models import DemoUser


@pytest.mark.asyncio
async def test_mysql_connection():
    connection = MySQLConnection(None)
    assert isinstance(connection, AbstractConnection)


class ConnectionTestCase(object):

    async def test_transaction(self):
        connection = MySQLConnection(None)
        connection.begin_transaction = mock.MagicMock(unsafe=True)
        connection.commit = mock.MagicMock(unsafe=True)
        connection.rollback = mock.MagicMock(unsafe=True)
        connection.insert = mock.MagicMock(return_value=1)

        async with await connection.transaction():
            await connection.insert(DemoUser())

        connection.begin_transaction.assert_called_once()
        connection.commit.assert_called_once()
        self.assertFalse(connection.rollback.called)

        connection.begin_transaction.reset_mock()
        connection.commit.reset_mock()
        connection.rollback.reset_mock()

        try:
            async with await connection.transaction():
                await connection.insert(DemoUser())
                raise Exception('foo')
        except Exception as e:
            self.assertEqual('foo', str(e))

        connection.begin_transaction.assert_called_once()
        connection.rollback.assert_called_once()
        self.assertFalse(connection.commit.called)
