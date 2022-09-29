from flask_restx import Resource
from flask_restx.reqparse import RequestParser

from __lib__.flask_fullstack import ResourceController
from common import sessionmaker, User
from .categories_db import Category

controller = ResourceController("category", sessionmaker=sessionmaker, path="/categories/")

category_parser: RequestParser = RequestParser()
category_parser.add_argument("name", type=str, required=True)


@controller.route("/")
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
