from logging import Logger

import aiomysql

from norm.connections.connections import Connection
from norm.query.query_compiler import QueryCompiler


class MySQLConnection(Connection):
    def __init__(self, conn, compiler: QueryCompiler = None, logger: Logger = None):
        super(MySQLConnection, self).__init__(conn, compiler=compiler, logger=logger)

        self._cursor = None

    async def new_cursor(self) -> aiomysql.DictCursor:
        if not self._cursor:
            print('new_cursor')
            self._cursor = await self._connection.cursor()
        return self._cursor
