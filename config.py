import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
top_level_dir = os.path.abspath(os.curdir)
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    STATIC_ROOT = os.path.join(basedir, "app/static")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "some random characters"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    AVATARS_SAVE_PATH = os.path.join(STATIC_ROOT, "avatars")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["gavrinjo@gmx.com"]
    UPLOADED_PATH = os.path.join(STATIC_ROOT, "uploads")
    ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
    POSTS_PER_PAGE = 10
