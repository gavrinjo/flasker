import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "some random characters"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    AVATARS_SAVE_PATH = os.path.join(basedir, "static/avatars")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["gavrinjo@gmx.com"]
    CKEDITOR_PKG_TYPE = os.environ.get('CKEDITOR_PKG_TYPE') or "standard"
    CKEDITOR_SERVE_LOCAL = os.environ.get("CKEDITOR_SERVE_LOCAL") or False
    CKEDITOR_HEIGHT = os.environ.get("CKEDITOR_HEIGHT")
    CKEDITOR_FILE_UPLOADER = "main.upload"
    CKEDITOR_FILE_BROWSER = "main.upload"
    UPLOADED_PATH = os.path.join(basedir, "uploads")
    POSTS_PER_PAGE = 5
