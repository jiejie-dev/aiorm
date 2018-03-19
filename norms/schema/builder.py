class SchemaBuilder(object):

    def create_tables(self, tables):
        return '\n'.join([self.create_table(x) for x in tables])

    def create_table(self, table):
        args = []
        for f_name, f in getattr(table, '__mappings__').items():
            args.append(str(f))
        sql = 'CREATE TABLE {} ({})'.format(getattr(table, '__table__'), ',\n\t'.join(args))
        return sql

    def drop_tables(self, tables):
        return '\n'.join(self.drop_table(x) for x in tables)

    def drop_table(self, table):
        return 'DROP TABLE {} IF EXISTS '.format(getattr(table, '__table__'))


class MysqlSchemaBuilder(SchemaBuilder):
    pass
