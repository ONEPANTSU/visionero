import datetime

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from database.database import session_maker
from src.models import ProgramHistory


class HistoryRepository:
    model = ProgramHistory

    async def add_running(
        self, program_name: str, time: datetime.datetime
    ) -> None | IntegrityError:
        try:
            async with session_maker() as session:
                await session.execute(
                    insert(self.model).values(program=program_name, time=time)
                )
                await session.commit()
        except IntegrityError as error:
            print(str(error))
            raise error

    async def get_all(self):
        async with session_maker() as session:
            result = await session.execute(select(self.model))
            return [model[0] for model in result.all()]
