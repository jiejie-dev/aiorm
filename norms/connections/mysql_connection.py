from logging import Logger

import aiomysql

from norms.connections.connections import Connection
from norms.query.query_compiler import QueryCompiler


class MysqlConnection(Connection):
    def __init__(self, conn, compiler: QueryCompiler = None, logger: Logger = None):
        super(MysqlConnection, self).__init__(conn, compiler=compiler, logger=logger)

    async def new_cursor(self) -> aiomysql.DictCursor:
        return await self._connection.cursor(aiomysql.DictCursor)
