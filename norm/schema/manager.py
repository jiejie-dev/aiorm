import logging

from norm.connections.mysql_connection import MySQLConnection
from norm.query import types
from norm.query.query_compiler import QueryCompiler, MySQLQueryCompiler
from norm.schema.builder import SchemaBuilder, MySQLSchemaBuilder

_logger = logging.getLogger('norm')


class SchemaManager(object):
    """ To manage tables, do actions linke create_table, drop_table."""

    def __init__(self, connection: MySQLConnection = None, builder: SchemaBuilder = None):
        self.connection = connection
        self.builder = builder or MySQLSchemaBuilder()

    def initalize(self, connection: MySQLConnection):
        self.connection = connection

    async def show_tables(self):
        sql = MySQLQueryCompiler.templates.get(types.SHOW_TABLES)
        rs = await self.connection.select(sql)

        def get_tables():
            for item in rs:
                yield [x for x in item.values()]

        tables = []
        [tables.extend(x) for x in get_tables()]
        return tables

    async def create_tables(self, tables, safe=True):
        sql = self.builder.create_tables(tables)
        try:
            await self.connection.execute(sql, None)
        except Exception as e:
            _logger.exception(e)
            if not safe:
                raise Exception('Create Table Error')

    async def drop_tables(self, tables, safe=True):
        sql = self.builder.drop_tables(tables)
        try:
            await self.connection.execute(sql)
        except Exception as e:
            _logger.exception(e)
            if not safe:
                raise Exception('Drop Table Error')

    async def add_table_column(self, table, column_name, column_type, column_default):
        pass
