import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback-secret"
    DATABASE = os.path.join(os.getcwd(), "instance", "logs.db")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True