import uuid

import aiomysql
import asyncio

import time

from norm.query.query_compiler import MySQLQueryCompiler
from sample.norm_bench import DemoUser


async def _main(loop):
    _pool = await aiomysql.create_pool(user='root', password='root', db='ncms', port=3309, loop=loop)
    # cur = await conn.cursor()
    conn = await _pool.acquire()
    compiler = MySQLQueryCompiler()

    t1 = time.time()
    for index in range(1000):
        cur = await conn.cursor()
        # sql = "INSERT INTO DemoUser (`id`, `name`) VALUES( %s, %s)"
        sql, args = compiler.compile_insert(DemoUser(name='UserName-{}'.format(uuid.uuid4)))
        await cur.execute(sql, args)

    t2 = time.time()
    print('NO_TRANSACTION: {}'.format(t2 - t1))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(loop))
