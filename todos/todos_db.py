from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, ForeignKey, sql, select
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from __lib__.flask_fullstack import Identifiable, PydanticModel
from common import Base, sessionmaker


class Todo(Base, Identifiable):
    __tablename__ = 'todos'

    # Vital
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start = Column(DateTime(), server_default=sql.func.now(), nullable=False)
    duration = Column(Integer, nullable=True)
    deleted = Column(Boolean, default=False, nullable=False)

    # Category-related
    category_name = Column(String(100), ForeignKey('categories.name'), nullable=False)
    categories = relationship('Category', backref='todos')

    # User-related
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    users = relationship('User', backref='todos')

    MainData = PydanticModel.column_model(
        id, name, start, duration, category_name, user_id
    )

    @classmethod
    def create(
            cls,
            session: sessionmaker,
            name: str,
            start: datetime,
            duration: int,
            category_name: str,
            user_id: int,
    ) -> Todo | None:
        return super().create(
            session,
            name=name,
            category_name=category_name,
            user_id=user_id,
            start=start,
            duration=duration,
            deleted=False,
        )

    @classmethod
    def get_list(cls, session: sessionmaker, user_id: int) -> list[Todo]:
        return session.get_all(select(cls).filter_by(user_id=user_id, deleted=False))

    @classmethod
    def get_by_date(cls, session: sessionmaker, date: str, user_id: int) -> list[Todo]:
        return session.get_all(select(cls).filter(
            cls.user_id == user_id,
            sql.func.date(cls.start) == sql.func.date(datetime.strptime(date, "%d/%m/%Y"))
        ))

    @classmethod
    def get_by_id(cls, session: sessionmaker, entry_id: int, user_id: int) -> Todo | None:
        return session.get_first(select(cls).filter_by(id=entry_id, user_id=user_id, deleted=False))
