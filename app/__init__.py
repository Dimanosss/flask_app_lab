import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

db = SQLAlchemy()
migrate = Migrate()

config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    if not config_name:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    config_class = config_map[config_name]
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.posts import post_bp
    app.register_blueprint(post_bp)

    @app.route("/")
    def index():
        from app.posts.models import Post
        from sqlalchemy import desc
        stmt = db.select(Post).where(Post.is_active.is_(True)).order_by(desc(Post.posted))
        posts = db.session.scalars(stmt).all()
        return render_template("posts/posts.html", posts=posts)

    @app.errorhandler(404)
    def nf(e):
        return render_template("404.html"), 404

    return app
