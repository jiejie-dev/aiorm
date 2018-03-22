class SchemaBuilder(object):
    """ A sql builder for SchemaManager"""

    def create_tables(self, tables):
        return ';'.join([self.create_table(x) for x in tables])

    def create_table(self, table):
        args = []
        for f_name, f in getattr(table, '__mappings__').items():
            args.append(str(f))
        sql = 'CREATE TABLE {} ({})'.format(getattr(table, '__table__'), ','.join(args))
        return sql

    def drop_tables(self, tables):
        return ';'.join(self.drop_table(x) for x in tables)

    def drop_table(self, table):
        return 'DROP TABLE IF EXISTS {}'.format(getattr(table, '__table__'))


class MySQLSchemaBuilder(SchemaBuilder):
    pass


class SqliteSchemaBuilder(SchemaBuilder):
    pass
