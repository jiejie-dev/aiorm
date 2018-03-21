from norm.schema.builder import SchemaBuilder
from tests.configtest import DemoUser, DemoUserProfile
from unittest import TestCase


class TestSchemaBuilderCase(TestCase):
    def test_schema_builder(self):
        builder = SchemaBuilder()
        sql = builder.create_table(DemoUser)
        assert sql is not None
        assert sql.startswith('CREATE TABLE Demo')
        sql = builder.drop_table(DemoUser)
        assert sql == 'DROP TABLE DemoUser IF EXISTS '

    def test_schema_with_foreign(self):
        builder = SchemaBuilder()
        self.assertRaises(Exception, builder.create_tables([DemoUserProfile]))
