import pytest
import mock

from norm.orm.connections import AbstractConnection, Connection
from sample.norm_bench import DemoUser


@pytest.mark.asyncio
async def test_mysql_connection():
    connection = Connection(None)
    assert isinstance(connection, AbstractConnection)


class ConnectionTestCase(object):

    def test_transaction(self):
        connection = Connection(None)
        connection.begin_transaction = mock.MagicMock(unsafe=True)
        connection.commit = mock.MagicMock(unsafe=True)
        connection.rollback = mock.MagicMock(unsafe=True)
        connection.insert = mock.MagicMock(return_value=1)

        with connection.transaction():
            connection.insert(DemoUser())

        connection.begin_transaction.assert_called_once()
        connection.commit.assert_called_once()
        self.assertFalse(connection.rollback.called)

        connection.begin_transaction.reset_mock()
        connection.commit.reset_mock()
        connection.rollback.reset_mock()

        try:
            with connection.transaction():
                connection.insert(DemoUser())
                raise Exception('foo')
        except Exception as e:
            self.assertEqual('foo', str(e))

        connection.begin_transaction.assert_called_once()
        connection.rollback.assert_called_once()
        self.assertFalse(connection.commit.called)
