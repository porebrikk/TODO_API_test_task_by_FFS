from os import getenv
from sys import modules

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

from __lib__.flask_fullstack import Flask
from __lib__.flask_fullstack.sqlalchemy import create_base, Sessionmaker, Session

load_dotenv(".env")

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db_url: str = getenv("DB_LINK", "sqlite:///app.db")
engine = create_engine(db_url, pool_recycle=280)  # echo=True
db_meta = MetaData(bind=engine, naming_convention=convention)
Base = create_base(db_meta)
sessionmaker = Sessionmaker(bind=engine, class_=Session)

app: Flask = Flask(__name__)
app.config["TESTING"] = "pytest" in modules.keys()
app.secrets_from_env("hope it's local")
app.configure_cors()

app.configure_error_handlers(print)
app.config["RESTX_INCLUDE_ALL_MODELS"] = True
