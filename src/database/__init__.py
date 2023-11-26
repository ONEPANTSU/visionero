from src.database.database import (
    Base,
    engine,
    get_async_session,
    session_maker,
)
from src.database.initializer import DataBaseInitializer

__all__ = [
    "engine",
    "session_maker",
    "Base",
    "get_async_session",
    "init_database",
]


def init_database(database_config):
    db_initializer = DataBaseInitializer(
        db_config=database_config, engine=engine, base=Base
    )
    db_initializer.initialize()
