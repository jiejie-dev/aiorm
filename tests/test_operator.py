import pytest
from aiomysql import create_pool

from norms.connections.connections import Connection
from norms.query.query_base import Query
from norms.query.query_compiler import MysqlQueryCompiler
from tests.base import configs, Demo
from tests.test_drivers import connection, driver


@pytest.mark.asyncio
async def test_insert(connection: Connection):
    data = Demo()
    r = await connection.insert(data)
    assert r == 1

@pytest.mark.asyncio
async def test_insert_original(event_loop):
    compiler = MysqlQueryCompiler()
    query, args = compiler.compile_insert(Demo())
    async with create_pool(host='127.0.0.1', port=3309,
                           user='root', password='root',
                           db='ncms', loop=event_loop) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("insert into Demo values( `%s` ,`%s` )", (None, 1))
                value = await cur.fetchone()