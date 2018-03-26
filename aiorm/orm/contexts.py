from aiorm.backends.base import DataBaseDriver, AbstractDataSet, QueryCompiler
from aiorm.orm.fields import UUIDField, StringField
from aiorm.orm.models import Model
from aiorm.orm.query import *


class DbSet(object):
    def __init__(self, model):
        self.model = model
        self.db = None  # type: DbContext

    async def add(self, data):
        sql, args = self.db.compiler.compile(InsertQuery(data))
        return await self.db.connection.execute(sql, args)

    async def remove(self, data):
        sql, args = self.db.compiler.compile(DeleteQuery(data))
        return await self.db.connection.execute(sql, args)

    async def count(self, query):
        sql, args = self.db.compiler.compile(query)
        return await self.db.connection.execute(sql, args)

    async def update(self, data):
        sql, args = self.db.compiler.compile(UpdateQuery(data))
        return await self.db.connection.execute(sql, args)

    def select_query(self) -> 'SelectQuery':
        return SelectQuery(self.model)

    def delete_query(self) -> 'DeleteQuery':
        return DeleteQuery(self.model)

    def insert_query(self) -> 'InsertQuery':
        return InsertQuery(self.model)

    def update_query(self) -> 'UpdateQuery':
        return UpdateQuery(self.model)

    async def run(self, query) -> AbstractDataSet:
        sql, args = self.db.compiler.compile(query)
        return await self.db.connection.execute(sql, args)


class DbContext(object):

    def __init__(self, **configs):
        self.configs = configs

        self.driver = DataBaseDriver.get(configs)
        self.compiler = QueryCompiler.get(self.driver.NAME)

        self.connection = self.driver.connection()

    async def begin(self, loop):
        await self.driver.initialize(loop, self.configs[self.driver.NAME])
        await self.connection.connect()
        await self.connection.begin_transaction()
        return self

    async def save_changes(self):
        await self.connection.commit()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.save_changes()
        await self.connection.close()
        return False

    def __getattribute__(self, item):
        prop = super(DbContext, self).__getattribute__(item)
        if isinstance(prop, DbSet):
            prop.db = self
        return prop

    async def create_tables(self, tables):
        for item in tables:
            sql, args = self.compiler.compile(CreateTableQuery(item))
            await self.connection.execute(sql, args)

    async def drop_tables(self, tables):
        for item in tables:
            sql, args = self.compiler.compile(DropTableQuery(item))
            await self.connection.execute(sql, args)
