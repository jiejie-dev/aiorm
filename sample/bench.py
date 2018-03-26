import asyncio

import time

from aiorm.orm.contexts import DbContext, DbSet
from aiorm.orm.fields import UUIDField, StringField
from aiorm.orm.models import Model
from sample.models import configs as demo_configs


class Demo(Model):
    id = UUIDField(primary_key=True)
    name = StringField()


class DemoDbContext(DbContext):
    demos = DbSet(Demo)


async def _main(loop):
    context = DemoDbContext(loop, **demo_configs)
    await context.begin()

    await context.drop_tables([Demo])
    await context.create_tables([Demo])

    t1 = time.time()

    for index in range(1000):
        demo = Demo()
        await context.demos.add(demo)
    await context.save_changes()

    t2 = time.time()
    print(t2 - t1)

    demo.name = 'jeremaihloo'
    await context.demos.update(demo)
    await context.save_changes()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(loop))
