from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory
from flask_login import current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import db
from app.main import bp
from app.main.forms import EditProfileForm
from app.models import User, Post



@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route("/")
@bp.route("/index")
def index():
    #user = User.query.filter_by(username=current_user.username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False)
    next_url = url_for("main.index", page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for("main.index", page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title="Home", posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.post.order_by(Post.timestamp.desc()).all()
    return render_template("user.html", title=user.username, user=user, posts=posts)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Update successful")
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)

