from norms.models.model_base import Model, IntegerField, StringField

configs = {
    'user': 'root',
    'password': 'root',
    'name': 'ncms',
    'port': 3309
}


class Demo(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
