from logging import Logger

import aiomysql

from norm.connections.connections import Connection
from norm.query.query_compiler import QueryCompiler


class MySQLConnection(Connection):
    def __init__(self, conn, compiler: QueryCompiler = None, logger: Logger = None):
        super(MySQLConnection, self).__init__(conn, compiler=compiler, logger=logger)

    async def new_cursor(self) -> aiomysql.DictCursor:
        return await self._connection.cursor(aiomysql.DictCursor)
