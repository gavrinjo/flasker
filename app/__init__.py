from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "auth.login"
migrate = Migrate(app, db)
mail = Mail(app)
avatars = Avatars(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app import models
