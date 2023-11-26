import asyncio

from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import create_async_engine


class DataBaseInitializer:
    def __init__(self, db_config, engine, base):
        self.db = db_config
        self.engine = engine
        self.base = base

    def initialize(self):
        asyncio.run(self._initialize_tasks())

    async def _initialize_tasks(self):
        await self._create_database_if_not_exists()
        await self._upgrade_tables()

    async def _create_database_if_not_exists(self):
        default_engine = create_async_engine(
            url=self.db.get_default_url(), poolclass=NullPool
        )
        async with default_engine.connect() as connection:
            async with connection.begin():
                existing_databases = await connection.execute(
                    text("SELECT datname FROM pg_catalog.pg_database")
                )
                if (self.db.name,) not in existing_databases:
                    await connection.execute(text("COMMIT"))
                    await connection.execute(
                        text(f"CREATE DATABASE {self.db.name}")
                    )

    async def _upgrade_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)
