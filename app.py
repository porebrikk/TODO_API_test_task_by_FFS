from common import db_url, db_meta
from main import app, socketio

if db_url == "sqlite:///app.db":
    db_meta.drop_all()
    db_meta.create_all()

if db_url == "sqlite:///test.db":
    db_meta.create_all()

if __name__ == "__main__":  # test only
    socketio.run(app=app)
