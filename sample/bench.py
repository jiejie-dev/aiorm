import asyncio

import time

from aiorm.orm.contexts import DbContext, DbSet
from sample.models import configs as demo_configs, DemoUser, DemoUserProfile, DemoPermission


class DemoDbContext(DbContext):
    users = DbSet(DemoUser)
    profiles = DbSet(DemoUserProfile)
    permissions = DbSet(DemoPermission)


async def _main(loop):
    context = DemoDbContext(loop, **demo_configs)
    await context.begin()

    await context.drop_tables([DemoUser, DemoUserProfile, DemoPermission])
    await context.create_tables([DemoUser, DemoUserProfile, DemoPermission])

    t1 = time.time()

    for index in range(1000):
        demo = DemoUser()
        await context.users.add(demo)
    await context.save_changes()

    t2 = time.time()
    print(t2 - t1)

    demo.name = 'jeremaihloo'
    await context.users.update(demo)
    await context.save_changes()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(loop))
