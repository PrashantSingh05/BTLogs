import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g
import os


def get_db():
    if 'db' not in g:
        db_url = os.environ.get("DATABASE_URL")

        if not db_url:
            raise Exception("DATABASE_URL not set")

        # 🔥 IMPORTANT CHANGE
        g.db = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        g.db.autocommit = True

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()