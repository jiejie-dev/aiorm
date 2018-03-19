from norms.schema.builder import SchemaBuilder
from tests.base import Demo


def test_builder():
    builder = SchemaBuilder()
    sql = builder.create_table(Demo)
    assert sql is not None
    assert sql.startswith('CREATE TABLE Demo')
    sql = builder.drop_table(Demo)
    assert sql == 'DROP TABLE Demo IF EXISTS '