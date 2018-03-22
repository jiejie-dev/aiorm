import uuid

import time
from peewee import UUIDField, CharField, Model, MySQLDatabase

configs = {
    'default': 'mysql',
    'mysql': {
        'user': 'root',
        'password': 'root',
        'port': 3309
    }
}

db = MySQLDatabase('ncms', user='root', password='root',
                   host='127.0.0.1', port=3309)

db.connect()


class DemoUser(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField()

    class Meta:
        database = db


def main():
    db.create_tables([DemoUser], safe=True)

    t1 = time.time()
    for index in range(1000):
        user = DemoUser(name='UserName-{}'.format(index))
        user.save()
    t2 = time.time()
    print('NO_TRANSACTION: {}'.format(t2 - t1))

    with db.transaction():
        for index in range(1000):
            user = DemoUser(name='UserName-{}'.format(index))
            user.save()

    t3 = time.time()
    print('ON_TRANSACTION: {}'.format(t3 - t2))


if __name__ == '__main__':
    main()
