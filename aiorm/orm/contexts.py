from aiorm.backends.base import DataBaseDriver, AbstractDataSet, QueryCompiler
from aiorm.orm.query import *


class DbSet(object):
    def __init__(self, model):
        self.model = model
        self.db = None  # type: DbContext

    async def get(self, **kwargs):
        query = SelectQuery(self.model, self)
        for key, val in kwargs:
            query.where(key == val)
        sql, args = self.db.compiler.compile(query)
        cursor = await self.db.connection.cursor(sql, args)
        return await cursor.fetch_one()

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
        return SelectQuery(self.model, self)

    def delete_query(self) -> 'DeleteQuery':
        return DeleteQuery(self.model, self)

    def insert_query(self) -> 'InsertQuery':
        return InsertQuery(self.model, self)

    def update_query(self) -> 'UpdateQuery':
        return UpdateQuery(self.model, self)

    async def run(self, query) -> AbstractDataSet:
        sql, args = self.db.compiler.compile(query)
        return await self.db.connection.cursor(sql, args)


class DbContext(object):

    def __init__(self, loop, **configs):
        self.configs = configs

        self.driver = DataBaseDriver.get(configs)
        self.compiler = QueryCompiler.get(self.driver.NAME)

        self.connection = self.driver.connection()

        self.loop = loop

    async def begin(self):
        await self.driver.initialize(self.loop, self.configs[self.driver.NAME])
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

    async def create_tables(self, tables, safe=True):
        e_tables = await self.show_tables()

        for item in tables:
            if safe and item.__table__ in e_tables:
                continue
            sql, args = self.compiler.compile(CreateTableQuery(item))
            await self.connection.execute(sql, args)

    async def drop_tables(self, tables):
        for item in tables:
            sql, args = self.compiler.compile(DropTableQuery(item))
            await self.connection.execute(sql, args)

    async def show_tables(self):
        sql, args = self.compiler.compile(ShowTablesQuery())
        dt = await self.connection.cursor(sql, args)
        tables = []
        for item in await dt.fetch_all():
            for k, v in item.items():
                tables.append(v)
        return tables
