from __future__ import annotations
from sqlalchemy import Column, ForeignKey, sql, select
from sqlalchemy.sql.sqltypes import Integer, String, Date, Time
from sqlalchemy.orm import relationship
from __lib__.flask_fullstack import Identifiable, PydanticModel
from .config import Base, sessionmaker


class Todo(Base, Identifiable):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_name = Column(String(100), ForeignKey('categories.name'), nullable=False)
    categories = relationship('Category', backref='todos')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    users = relationship('User', backref='todos')
    start_date = Column(Date(), server_default=sql.func.current_date())
    start_time = Column(Time(timezone=True), server_default=sql.func.current_time())
    end_time = Column(Time(timezone=True), nullable=True)

    MainData = PydanticModel.column_model(id, name, category_name, user_id, start_date, start_time, end_time)

    @classmethod
    def check_user(cls, session: sessionmaker, user) -> Todo | None:
        return session.get_all(select(cls).filter_by(user_id=user))

    @classmethod
    def create(cls, session: sessionmaker, name: str, category_name: str, user_id: int,
               start_date: str, start_time: str, end_time: str) -> Todo | None:
        return super().create(session, name=name, category_name=category_name, user_id=user_id,
                              start_date=start_date, start_time=start_time, end_time=end_time)

    @classmethod
    def get_by_id(cls, session: sessionmaker, entry_id: int, user) -> Todo | None:
        return session.get_first(select(cls).filter_by(id=entry_id, user_id=user))

    @classmethod
    def find_by_date(cls, session, entry_date: str, user) -> Todo | None:
        return session.get_all(select(cls).filter_by(user_id=user, start_date=entry_date))


class Category(Base, Identifiable):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    MainData = PydanticModel.column_model(id, name)

    @classmethod
    def get_list(cls, session: sessionmaker) -> Category | None:
        return session.get_all(select(cls))

    @classmethod
    def create(cls, session: sessionmaker, name: str) -> Category | None:
        return super().create(session, name=name)

    @classmethod
    def get_by_id(cls, session: sessionmaker, entry_id: int) -> Category | None:
        return session.get_first(select(cls).filter_by(id=entry_id))

    @classmethod
    def get_by_name(cls, session: sessionmaker, entry_name: str) -> Category | None:
        return session.get_first(select(cls).filter_by(name=entry_name))
