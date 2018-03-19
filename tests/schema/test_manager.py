import pytest

from norms.schema.manager import SchemaManager
from tests.base import Demo
from tests.test_drivers import driver, connection


@pytest.fixture()
async def schema_manager(connection):
    manager = SchemaManager(connection)
    return manager


@pytest.mark.asyncio
async def test_show_tables(schema_manager):
    assert schema_manager is not None
    tables = await schema_manager.show_tables()

    assert isinstance(tables, list)
    assert len(tables) > 0


@pytest.mark.asyncio
async def test_create_tables(schema_manager: SchemaManager):
    await schema_manager.create_tables([Demo])
