from norm.schema.builder import SchemaBuilder
from sample.models import DemoUser, DemoUserProfile
from unittest import TestCase

class TestSchemaBuilderCase(TestCase):
    def setUp(self):
        self.builder = SchemaBuilder()

    def test_schema_builder(self):
        sql = self.builder.create_table(DemoUser)
        assert sql == """CREATE TABLE DemoUser (
	id VARCHAR(40) primary key,
	name varchar(100) 
)"""
        sql = self.builder.drop_table(DemoUser)
        assert sql == """DROP TABLE DemoUser IF EXISTS """

    def test_drop_tables(self):
        sql = self.builder.drop_tables([DemoUser, DemoUserProfile])

    def test_schema_with_foreign(self):
        self.assertRaises(Exception, self.builder.create_tables([DemoUserProfile]))
