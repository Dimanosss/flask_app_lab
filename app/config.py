import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR.parent / "instance"

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{INSTANCE_DIR/'data.sqlite'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG=True

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    WTF_CSRF_ENABLED=False

class ProductionConfig(Config):
    DEBUG=False
