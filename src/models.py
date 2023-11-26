import datetime
from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class ProgramHistory(Base):
    __tablename__ = "program_history"

    id: Mapped[int_pk]
    program: Mapped[str]
    time: Mapped[datetime.datetime]
