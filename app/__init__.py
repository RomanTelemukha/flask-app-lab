from sqlalchemy.orm import DeclarativeBase
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from .config import config

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })
    
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "default")

    app = Flask(__name__)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import register_routes
    register_routes(app)

    from .users.views import users_bp
    from .products.views import products_bp
    from .posts import post_bp, models

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(products_bp, url_prefix="/product", name="product")
    app.register_blueprint(post_bp, url_prefix="/post")
    app.register_blueprint(post_bp, url_prefix="/posts", name="post")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


app = create_app()
