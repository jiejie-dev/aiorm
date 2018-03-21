import pytest

from norm.connections.connections import IConnection, Connection
from norm.connections.mysql_connection import MySQLConnection
import mock

from tests.configtest import Demo


@pytest.mark.asyncio
async def test_mysql_connection():
    connection = MySQLConnection(None)
    assert isinstance(connection, IConnection)


class ConnectionTestCase(object):

    def test_transaction(self):
        connection = Connection(None)
        connection.begin_transaction = mock.MagicMock(unsafe=True)
        connection.commit = mock.MagicMock(unsafe=True)
        connection.rollback = mock.MagicMock(unsafe=True)
        connection.insert = mock.MagicMock(return_value=1)

        with connection.transaction():
            connection.insert(Demo())

        connection.begin_transaction.assert_called_once()
        connection.commit.assert_called_once()
        self.assertFalse(connection.rollback.called)

        connection.begin_transaction.reset_mock()
        connection.commit.reset_mock()
        connection.rollback.reset_mock()

        try:
            with connection.transaction():
                connection.insert(Demo())
                raise Exception('foo')
        except Exception as e:
            self.assertEqual('foo', str(e))

        connection.begin_transaction.assert_called_once()
        connection.rollback.assert_called_once()
        self.assertFalse(connection.commit.called)
