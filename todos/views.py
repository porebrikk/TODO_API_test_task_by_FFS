from flask_restx import Resource
from flask_restx.reqparse import RequestParser

from __lib__.flask_fullstack import ResourceController
from common import sessionmaker, User
from .todos_db import Todo, Category

controller = ResourceController('todo', sessionmaker=sessionmaker, path='/')

todo_parser: RequestParser = RequestParser()
todo_parser.add_argument('name', type=str, required=True)
todo_parser.add_argument('category_name', type=str, required=True)
todo_parser.add_argument('start_date', type=str)
todo_parser.add_argument('start_time', type=str)
todo_parser.add_argument('end_time', type=str)

todo_date_parser: RequestParser = RequestParser()
todo_date_parser.add_argument('start_date', type=str, required=True)

category_parser: RequestParser = RequestParser()
category_parser.add_argument('name', type=str, required=True)


@controller.route('/todos')
class TodoList(Resource):

    @controller.jwt_authorizer(User)
    @controller.marshal_list_with(Todo.MainData)
    def get(self, session: sessionmaker, user: User):
        return Todo.check_user(session, user.id)

    @controller.jwt_authorizer(User)
    @controller.argument_parser(todo_parser)
    @controller.marshal_with(Todo.MainData)
    def post(self, session, name: str, category_name: str, start_date: str, start_time: str,
             end_time: str, user: User):
        if Category.get_by_name(session, category_name) is None:
            Category.create(session, category_name)
        return Todo.create(session, name, category_name, user.id, start_date, start_time, end_time)


@controller.route('/todos/date')
class TodoDate(Resource):

    @controller.jwt_authorizer(User)
    @controller.argument_parser(todo_date_parser)
    @controller.marshal_list_with(Todo.MainData)
    def post(self, session, start_date: str, user: User):
        return Todo.find_by_date(session, start_date, user.id)


@controller.route('/categories')
class CategoryList(Resource):

    @controller.jwt_authorizer(User, check_only=True)
    @controller.marshal_list_with(Category.MainData)
    def get(self, session):
        return Category.get_list(session)

    @controller.jwt_authorizer(User, check_only=True)
    @controller.argument_parser(category_parser)
    @controller.marshal_with(Category.MainData)
    def post(self, session, name: str):
        return Category.create(session, name)


@controller.route('/todos/<int:entry_id>')
class Todos(Resource):

    @controller.jwt_authorizer(User)
    @controller.marshal_with(Todo.MainData)
    def get(self, session, entry_id: int, user: User):
        if (todo := Todo.get_by_id(session, entry_id, user.id)) is None:
            raise Exception('ID does not exist')
        return todo

    @controller.jwt_authorizer(User)
    @controller.argument_parser(todo_parser)
    @controller.marshal_with(Todo.MainData)
    def put(self, session, entry_id: int, name: str, category_name: str, start_date: str,
            start_time: str, end_time: str, user: User):
        if (update_todo := Todo.get_by_id(session, entry_id, user.id)) is None:
            raise Exception('ID does not exist')
        if Category.get_by_name(session, category_name) is None:
            Category.create(session, category_name)
        update_todo.name = name if name else update_todo.name
        update_todo.category_name = category_name if category_name else update_todo.category_name
        update_todo.user_id = user.id
        update_todo.start_date = start_date if start_date else update_todo.start_date
        update_todo.start_time = start_time if start_time else update_todo.start_time
        update_todo.end_time = end_time if end_time else update_todo.end_time
        return update_todo

    @controller.jwt_authorizer(User)
    @controller.marshal_with(Todo.MainData)
    def delete(self, session, entry_id: int, user: User):
        if (deleted_todo := Todo.get_by_id(session, entry_id, user.id)) is None:
            raise Exception('ID does not exist')
        session.delete(deleted_todo)
        session.flush()
        return deleted_todo


@controller.route('/categories/<int:entry_id>')
class Categories(Resource):

    @controller.jwt_authorizer(User, check_only=True)
    @controller.marshal_with(Category.MainData)
    def get(self, session, entry_id: int):
        if (category := Category.get_by_id(session, entry_id)) is None:
            raise Exception("ID does not exist")
        return category
