from __future__ import annotations

from flask_restx import Resource
from flask_restx.reqparse import RequestParser

from datetime import datetime

from __lib__.flask_fullstack import ResourceController
from common import sessionmaker, User
from .todos_db import Todo
from .categories_db import Category

controller = ResourceController('todo', sessionmaker=sessionmaker, path='/todos/')


@controller.route('/')
class TodoList(Resource):
    parser: RequestParser = RequestParser()
    parser.add_argument("name", type=str, required=True)
    parser.add_argument("start", type=str)
    parser.add_argument("duration", type=int)
    parser.add_argument("category_name", type=str, required=True)

    dateparser: RequestParser = RequestParser()
    dateparser.add_argument("date", type=str)

    @controller.jwt_authorizer(User)
    @controller.argument_parser(dateparser)
    @controller.marshal_list_with(Todo.MainData)
    def get(self, session: sessionmaker, date: str, user: User):
        if date is None:
            todos = Todo.get_list(session, user.id)
        else:
            todos = Todo.get_by_date(session, date, user.id)
        return todos

    @controller.jwt_authorizer(User)
    @controller.argument_parser(parser)
    @controller.marshal_with(Todo.MainData)
    def post(
            self,
            session,
            name: str,
            category_name: str,
            start: str | None,
            duration: int | None,
            user: User,
    ):
        if Category.get_by_name(session, category_name) is None:
            Category.create(session, category_name)
        if start is not None:
            start = datetime.strptime(start, "%d/%m/%Y %H:%M:%S")
        return Todo.create(session, name, start, duration, category_name, user.id)


@controller.route('/<int:todo_id>/')
class Todos(Resource):
    parser: RequestParser = RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("start", type=str)
    parser.add_argument("duration", type=int)
    parser.add_argument("category_name", type=str)

    @controller.doc_abort(404, "Todo not found")
    @controller.jwt_authorizer(User)
    @controller.marshal_with(Todo.MainData)
    def get(self, session, todo_id: int, user: User):
        todo = Todo.get_by_id(session, todo_id, user.id)
        if todo is None or todo.user_id != user.id:
            controller.abort(404, "Todo not found")
        return todo

    @controller.doc_abort(404, "Todo not found")
    @controller.jwt_authorizer(User)
    @controller.argument_parser(parser)
    @controller.marshal_with(Todo.MainData)
    def put(
            self,
            session,
            todo_id: int,
            name: str | None,
            start: str | None,
            duration: int | None,
            category_name: str | None,
            user: User,
    ):
        todo = Todo.get_by_id(session, todo_id, user.id)
        if todo is None or todo.user_id != user.id:
            controller.abort(404, "Todo not found")
        if start is not None:
            start = datetime.strptime(start, "%d/%m/%Y %H:%M:%S")
            todo.start = start
        if Category.get_by_name(session, category_name) is None:
            Category.create(session, category_name)

        todo.name = name or todo.name
        todo.category_name = category_name or todo.category_name
        todo.duration = duration or todo.duration
        return todo

    @controller.doc_abort(404, "Todo not found")
    @controller.jwt_authorizer(User)
    def delete(self, session, todo_id: int, user: User):
        todo = Todo.get_by_id(session, todo_id, user.id)
        if todo is None or todo.user_id != user.id:
            controller.abort(404, "Todo not found")
        todo.deleted = True
        return {"a": "Success"}, 200
