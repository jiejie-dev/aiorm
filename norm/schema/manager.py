import logging

from norm.connections.mysql_connection import MySQLConnection
from norm.query import types
from norm.query.query_compiler import QueryCompiler, MySQLQueryCompiler

_logger = logging.getLogger('norm')


class SchemaManager(object):
    """ To manage tables, do actions linke create_table, drop_table."""

    def __init__(self, connection: MySQLConnection = None):
        self.connection = connection

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
        def get_create_table_sql():
            for item in tables:
                args = []
                for f_name, f in getattr(item, '__mappings__').items():
                    args.append(str(f))
                sql = 'CREATE TABLE {} ({})'.format(getattr(item, '__table__'), ',\n\t'.join(args))
                yield sql

        sqls = list(get_create_table_sql())
        try:
            await self.connection.execute('\n'.join(sqls), None)
        except Exception as e:
            _logger.exception(e)
            if not safe:
                raise Exception('Create Table Error')

    async def drop_tables(self, tables, safe=True):
        def get_drop_table_sql():
            for item in tables:
                sql = 'DROP TABLE {}'.format(getattr(item, '__table__'))
                yield sql

        sqls = list(get_drop_table_sql())
        try:
            await self.connection.execute('\n'.join(sqls))
        except Exception as e:
            _logger.exception(e)
            if not safe:
                raise Exception('Create Table Error')

    async def add_table_column(self, table, column_name, column_type, column_default):
        pass
