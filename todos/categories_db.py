from __future__ import annotations

from sqlalchemy import Column, select
from sqlalchemy.sql.sqltypes import Integer, String


from __lib__.flask_fullstack import Identifiable, PydanticModel
from common import Base, sessionmaker


class Category(Base, Identifiable):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    MainData = PydanticModel.column_model(id, name)

    @classmethod
    def get_list(cls, session: sessionmaker) -> Category | None:
        return session.get_all(select(cls))

    @classmethod
    def get_by_name(
            cls,
            session: sessionmaker,
            entry_name: str,
    ) -> Category | None:
        return session.get_first(select(cls).filter_by(name=entry_name))

    @classmethod
    def create(cls, session: sessionmaker, name: str) -> Category | None:
        return super().create(session, name=name)
