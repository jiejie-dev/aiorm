import asyncio

from norm.models.model_base import Model
from norm.models.fields import StringField, UUIDField, ForeignKeyField

import time

from norm.drivers import MySQLDataBaseDriver
from norm.schema.manager import SchemaManager
from sample.models import DemoUserProfile, DemoUser, DemoPermission, configs


async def _main(loop):
    driver = MySQLDataBaseDriver()
    await driver.initialize(loop=loop, configs=configs['mysql'])
    db = await driver.get_connection()
    schema = SchemaManager(db)
    await schema.drop_tables([DemoUser, DemoUserProfile, DemoPermission])
    await schema.create_tables([DemoUser, DemoUserProfile, DemoPermission])

    db = await driver.get_connection()

    t1 = time.time()
    for index in range(1000):
        user = DemoUser(name="UserName-{}".format(index))
        await db.insert(user)

    t2 = time.time()
    print('NO_TRANSACTION: {}'.format(t2 - t1))

    async with db.transaction():
        for index in range(1001, 2000):
            user = DemoUser(name="UserName-{}".format(index))
            await db.insert(user)

    t3 = time.time()
    print('ON_TRANSACTION: {}'.format(t3 - t2))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(loop))


if __name__ == '__main__':
    main()
