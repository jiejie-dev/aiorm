import logging

from norms.connections.mysql_connection import MysqlConnection
from norms.query import types
from norms.query.query_compiler import QueryCompiler, MysqlQueryCompiler

_logger = logging.getLogger('norms')


class SchemaManager(object):
    def __init__(self, connection: MysqlConnection):
        self.connection = connection

    async def show_tables(self):
        sql = MysqlQueryCompiler.templates.get(types.SHOW_TABLES)
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
