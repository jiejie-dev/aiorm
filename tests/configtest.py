from norm.models.model_base import Model
from norm.models.fields import StringField, UUIDField, ForeignKeyField

configs = {
    'default': 'mysql',
    'mysql': {
        'user': 'root',
        'password': 'root',
        'name': 'ncms',
        'port': 3309
    }
}


class DemoUser(Model):
    id = UUIDField(primary_key=True)
    name = StringField()


class DemoUserProfile(Model):
    id = UUIDField(primary_key=True)
    user = ForeignKeyField(DemoUser, related_name='profile')

class DemoPermission(Model):
    id = UUIDField(primary_key=True)
    profile = ForeignKeyField(DemoUserProfile, related_name='permission')