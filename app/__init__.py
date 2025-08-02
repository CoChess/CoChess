import sqlite3
from flask import Flask, g
from app.config import Config
from app.routes.routes import configure_routes

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY

    app.teardown_appcontext(close_db)
    app.get_db = get_db

    configure_routes(app)

    return app

