from norms.models.model_base import Model, StringField, IntegerField
from norms.query.query_base import Query
from norms.query.query_compiler import MysqlQueryCompiler
import pytest


class Demo(Model):
    id = IntegerField(primary_key=True)
    name = StringField()


@pytest.fixture()
def query_compiler():
    return MysqlQueryCompiler()


def test_select_query_compile():
    compiler = MysqlQueryCompiler()
    query = Query(Demo).select()
    rs = compiler.compile(query)
    assert rs[0].lower() == 'SELECT * FROM Demo'.lower()
    assert len(rs[1]) == 0


def test_select_query():
    query = Query(Demo).select().where(Demo.name == 'lujiejie')
    compiler = MysqlQueryCompiler()
    rs = compiler.compile(query)
    assert rs[0].lower() == "SELECT * FROM Demo WHERE ( demo.name = ? )".lower()
    assert rs[1][0] == "lujiejie"


def test_insert_query(query_compiler: MysqlQueryCompiler):
    data = Demo()
    data.name = 'lujiejie'
    data.id = 10
    template, args = query_compiler.compile_insert(data)
    assert isinstance(template, str) and template.lower().startswith('insert into')
    assert args == ['lujiejie', 10]
