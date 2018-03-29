import pytest

from aiorm.backends.mysql.compiler import MySQLQueryCompiler
from aiorm.orm.query import _foregin_fields, SelectQuery
from sample.models import DemoUserProfile, DemoUser, DemoPermission


@pytest.fixture()
def query_compiler():
    return MySQLQueryCompiler()


def test_select_query_compile():
    compiler = MySQLQueryCompiler()
    query = SelectQuery(DemoUser)
    rs = compiler.compile(query)
    assert rs[0].lower() == 'SELECT * FROM DemoUser'.lower()
    assert len(rs[1]) == 0


def test_select_query():
    query = SelectQuery(DemoUser).where(DemoUser.name == 'lujiejie')
    compiler = MySQLQueryCompiler()
    rs = compiler.compile(query)
    assert rs[0].lower() == "SELECT * FROM DemoUser WHERE ( demouser.name = %s )".lower()
    assert rs[1][0] == "lujiejie"


def test_insert_query(query_compiler: MySQLQueryCompiler):
    data = DemoUser()
    data.name = 'lujiejie'
    template, args = query_compiler.compile_insert(data)
    assert isinstance(template, str) and template.lower().startswith('insert into')
    assert args == ('lujiejie', data.id)


def test_select_foreign():
    query = SelectQuery(DemoUser).where(DemoUserProfile.user == 'jeremaihloo')
    compiler = MySQLQueryCompiler()
    rs = compiler.compile(query)
    print(rs)


def test_join():
    query = SelectQuery(DemoUser).join(DemoUserProfile).join(DemoPermission).where(
        DemoUserProfile.name == 'jeremaihloo'
    )
    compiler = MySQLQueryCompiler()
    rs = compiler.compile(query)
    print(rs)


def test_foreign_fields():
    fields = _foregin_fields(DemoUserProfile)
    assert len(list(fields)) == 1


def test_query_clone():
    query_1 = SelectQuery(DemoUser).join(DemoUserProfile)
    query_2 = query_1.where(DemoUser.name == 'jeremaihloo')
    assert query_1 != query_2
    assert query_1 is not query_2
    compiler = MySQLQueryCompiler()
    print(compiler.compile(query_2))
    print(compiler.compile(query_2))
