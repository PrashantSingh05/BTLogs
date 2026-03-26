from flask import Flask
from .config import Config
from .database.db import get_db
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


csrf = CSRFProtect()
limiter = Limiter(get_remote_address)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    limiter.init_app(app)

    # 🔥 REGISTER ROUTES
    from .routes.auth_routes import auth_bp
    from .routes.log_routes import log_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(admin_bp)

    # 🔥 AUTO CREATE TABLES
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            category TEXT,
            action_type TEXT,
            reason TEXT,
            downtime FLOAT,
            impact_level TEXT,
            tags TEXT,
            system_name TEXT,
            created_by TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        db.commit()

    return app