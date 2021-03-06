import jwt
from datetime import datetime
from time import time
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin
from flask import current_app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"User:{self.username} Email:{self.email}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id, "exp": time() + expires_in}, current_app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[
                            "HS256"])["reset_password"]
        except:
            return
        return User.query.get(id)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&r=x&s={size}"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # image = db.Column(db.)
    title = db.Column(db.String(64))
    subtitle = db.Column(db.String(128))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Title:{self.title} Subtitle:{self.subtitle} Body:{self.body}"


class Comment(db.Model):
    _N = 6

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) # Author ID
    post_id = db.Column(db.Integer, db.ForeignKey("post.id")) # Post ID
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id")) # Parent Comment ID
    replies = db.relationship("Comment", backref=db.backref("parent", remote_side=[id]), lazy="dynamic")

    def __repr__(self):
        return f"User:{User.query.filter_by(id=self.user_id).first().username}, Comment:{self.text}"

    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.parent.path + "." if self.parent else ""
        self.path = prefix + "{:0{}d}".format(self.id, self._N)
        db.session.commit()

    def level(self):
        return len(self.path) // self._N - 1