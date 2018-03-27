import pytest

from sample.bench import DemoDbContext
from sample.models import configs, DemoUser

pytestaio = pytest.mark.asyncio


@pytest.fixture()
async def context(event_loop):
    ctx = DemoDbContext(event_loop, **configs)
    await ctx.begin()
    return ctx


@pytestaio
async def test_context_show_tables(context: DemoDbContext):
    tables = await context.show_tables()
    assert isinstance(tables, list)


@pytestaio
async def test_context_create_table(context: DemoDbContext):
    await context.create_tables([DemoUser])
    tables = await context.show_tables()
    assert 'DemoUser' in tables
