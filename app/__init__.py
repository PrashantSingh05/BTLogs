from flask import Flask
from .config import Config
from .database.db import close_db
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CSRF protection
    csrf.init_app(app)

    # Enable rate limiting
    limiter.init_app(app)

    # Security headers
    @app.after_request
    def apply_security_headers(response):
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    app.teardown_appcontext(close_db)

    # Register routes
    from .routes.log_routes import log_bp
    from .routes.auth_routes import auth_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(log_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app