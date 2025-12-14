import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

# Налаштування naming convention для обмежень
metadata = MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Базова конфігурація
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(app.instance_path, "data.sqlite")}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Створення папки instance, якщо не існує
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Реєстрація блюпринтів
    from app.products import products_bp
    app.register_blueprint(products_bp, url_prefix='/products')
    
    # Імпорт моделей для Flask-Migrate
    from app.products import models  # noqa
    
    @app.route('/')
    def index():
        return '<h1>Lab7 Flask Project</h1><p><a href="/products">Перейти до продуктів</a></p>'
    
    return app
