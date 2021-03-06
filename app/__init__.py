from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_admin import Admin


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page"
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
avatars = Avatars()
admin = Admin()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    avatars.init_app(app)
    admin.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.content import bp as content_bp
    app.register_blueprint(content_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    return app

from app import models
