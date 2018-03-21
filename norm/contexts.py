from norm.models.model_base import Model, IntegerField, StringField, UUIDField


class DbSet(object):
    def __init__(self, model):
        self.model = model

    def add(self, data):
        pass

    def remove(self, data):
        pass

    def count(self):
        pass

    def update(self, data):
        pass


class DbContext(object):

    def initalize(self):
        pass

    def save_changes(self):
        pass


class Demo(Model):
    id = UUIDField(primary_key=True)
    name = StringField()


class DemoDbContext(DbContext):
    demos = DbSet(Demo)


if __name__ == '__main__':
    demo = Demo()
    context = DemoDbContext()

    context.database.drop_tables([Demo])
    context.database.create_tables([Demo])

    context.demos.add(demo)
    context.save_changes()
    demo.name = 'jeremaihloo'
    context.demos.update(demo)
    context.save_changes()
