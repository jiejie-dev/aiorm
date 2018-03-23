import functools
import sqlparse

_format_sql = functools.partial(sqlparse.format, reindent=True)


def format_sql(sql):
    return _format_sql(sql.lower())
