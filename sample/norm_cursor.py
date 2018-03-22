import uuid

import aiomysql
import asyncio

import time

from norm.drivers import MySQLDataBaseDriver
from norm.query.query_compiler import MySQLQueryCompiler
from sample.norm_bench import DemoUser, configs


async def _main(loop):

    driver = MySQLDataBaseDriver()
    await driver.initialize(loop=loop, configs=configs['mysql'])

    compiler = MySQLQueryCompiler()

    conn = await driver.get_connection()
    c = await aiomysql.connect(user='root', password='root', port=3309)

    t1 = time.time()

    for index in range(1000):

        # await c.cursor()

        # await conn._connection.cursor()
        cur = await conn.new_cursor()
        print(cur)
        # cur = await conn._connection.cursor()

        # sql = "INSERT INTO DemoUser (`id`, `name`) VALUES( %s, %s)"
        sql, args = compiler.compile_insert(DemoUser(name='UserName-{}'.format(index)))
        print(sql, args)
        # cur.execute(sql, args)
        await cur.execute("INSERT INTO DemoUser (`id`, `name`) VALUES( %s, %s)", (str(uuid.uuid4()), str(uuid.uuid4())))

    t2 = time.time()
    print('NO_TRANSACTION: {}'.format(t2 - t1))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(loop))
