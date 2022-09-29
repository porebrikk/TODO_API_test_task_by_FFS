from datetime import timedelta

from __lib__.flask_fullstack import SocketIO
from common import app
from common import db_meta, db_url  # noqa
from users import reglog_namespace
from todos import todos_namespace, categories_namespace

jwt = app.configure_jwt_with_loaders(["cookies"], timedelta(hours=72), lambda *x: print(x[1]), csrf_protect=False)
api = app.configure_restx()

api.add_namespace(reglog_namespace)
api.add_namespace(todos_namespace)
api.add_namespace(categories_namespace)

socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True, remove_ping_pong_logs=True)
