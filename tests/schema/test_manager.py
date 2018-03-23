import pytest

from norm.orm.schema import SchemaManager, SchemaBuilder
from sample.models import DemoUser


@pytest.fixture()
async def schema_manager(connection):
    manager = SchemaManager(connection, SchemaBuilder())
    return manager


@pytest.mark.asyncio
async def test_show_tables(schema_manager):
    assert schema_manager is not None
    tables = await schema_manager.show_tables()

    assert isinstance(tables, list)
    assert len(tables) > 0


@pytest.mark.asyncio
async def test_create_tables(schema_manager: SchemaManager):
    await schema_manager.create_tables([DemoUser])
