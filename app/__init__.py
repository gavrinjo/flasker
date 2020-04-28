from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"
migrate = Migrate(app, db)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


from app import routes, models
