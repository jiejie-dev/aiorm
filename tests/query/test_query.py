from norm.models.model_base import Model
from norm.models.fields import StringField, IntegerField
from norm.query.query_base import Query, _foregin_fields
from norm.query.query_compiler import MySQLQueryCompiler
import pytest

from sample.norm_bench import DemoUserProfile, DemoUser, DemoPermission


@pytest.fixture()
def query_compiler():
    return MySQLQueryCompiler()


def test_select_query_compile():
    compiler = MySQLQueryCompiler()
    query = Query(DemoUser).select()
    rs = compiler.compile(query)
    assert rs[0].lower() == 'SELECT * FROM Demo'.lower()
    assert len(rs[1]) == 0


def test_select_query():
    query = Query(DemoUser).select().where(DemoUser.name == 'lujiejie')
    compiler = MySQLQueryCompiler()
    rs = compiler.compile(query)
    assert rs[0].lower() == "SELECT * FROM DemoUser WHERE ( demouser.name = ? )".lower()
    assert rs[1][0] == "lujiejie"


def test_insert_query(query_compiler: MySQLQueryCompiler):
    data = DemoUser()
    data.name = 'lujiejie'
    template, args = query_compiler.compile_insert(data)
    assert isinstance(template, str) and template.lower().startswith('insert into')
    assert args == ('lujiejie', data.id)


def test_select_foreign():
    query = Query(DemoUser).select().where(DemoUserProfile.user == 'jeremaihloo')
    compiler = MySQLQueryCompiler()
    rs = compiler.compile(query)
    print(rs)


def test_join():
    query = Query(DemoUser).select().join(DemoUserProfile).join(DemoPermission).where(
        DemoUserProfile.name == 'jeremaihloo'
    )
    compiler = MySQLQueryCompiler()
    rs = compiler.compile(query)
    print(rs)


def test_foreign_fields():
    fields = _foregin_fields(DemoUserProfile)
    assert len(list(fields)) == 1
