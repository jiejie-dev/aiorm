from norms.models.model_base import create_args_string
from norms.query import types
from norms.query.query_base import Query


class QueryCompiler(object):
    maker = '?'

    def compile(self, query) -> str:
        NotImplementedError()

    def raw_sql(self, query) -> str:
        if isinstance(query, str):
            return query

        sql = self.compile(query)
        for item in query._args:
            sql = sql.replace(self.maker, item, 1)
        return sql


class MysqlQueryCompiler(QueryCompiler):
    templates = {
        types.SELECT: "SELECT {query_fields} FROM {TABLE_NAME}{WHERE}{order_by}{LIMIT}{OFFSET}".lower(),
        types.INSERT: "INSERT INTO table_name ({FIELDS}) VALUES ({VALUES})".lower(),
        types.SHOW_TABLES: "SHOW TABLES"
    }

    def compile(self, query):
        if query.method == types.SELECT:
            return self.compile_select_query(query)
        if query.method == types.INSERT:
            return self.compile_insert(query.data)
        return query, None

    def compile_select_query(self, query: Query):
        if query._where is not None:
            where_strs, where_args = query._where.build()
            query._args.extend(where_args)
            where_strs = ' ' + where_strs
        else:
            where_strs = ''

        orderby_str = ' ORDER BY ' + ' and '.join(query._orderby) if len(query._orderby) > 0 else ''

        limit_str = ' LIMIT {}'.format(query._limit) if query._limit > 0 else ''

        offset_str = ' OFFSET {}'.format(query._offset) if query._offset > 0 else ''

        return self.templates[query.method].format(query_fields='*', table_name=query.table_name,
                                                   where=' WHERE' + where_strs, order_by=orderby_str,
                                                   limit=limit_str, offset=offset_str), tuple(query._args)

    def compile_insert(self, data):
        table_name = getattr(data, '__table__')
        primary_key = getattr(data, '__primary_key__')
        fields = getattr(data, '__fields__')
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        insert_template = 'insert into `%s` (%s, `%s`) values (%s)' % (
            table_name, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        args = list(map(data.get_value_or_default, data.__fields__))
        args.append(data.get_value_or_default(data.__primary_key__))
        return insert_template.replace(self.maker, '%s'), tuple(args)

    def compile_update(self, data):
        args = list(map(data.get_value, data.__fields__))
        args.append(data.get_value(data.__primary_key__))
        template = 'update `%s` set %s where `%s`=?' % (
            data.__table__, ', '.join(map(lambda f: '`%s`=?' % (self.__mappings__.get(f).name or f), data.__fields__)),
            data.__primary_key__)
        return template, tuple(args)
