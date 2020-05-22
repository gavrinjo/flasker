import os
import uuid
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory
from flask_login import current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
# from flask_ckeditor import upload_fail, upload_success
from app import db
from app.main import bp, handlers
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post
# from flask_uploads import UploadSet



@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=handlers.img_src(form.post.data), author=current_user)
        # print(post)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!!")
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False)
    next_url = url_for("main.index", page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for("main.index", page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title="Home", form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

"""
@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOADED_PATH"], filename)


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@bp.route("/upload", methods=["POST", "GET"])
def upload():
    form = PostForm()
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename): 
            #if os.path.exists(current_app.config["UPLOADED_PATH"] + "/" + file.filename): # if image with same name exists
            _dot = file.filename.find(".")
            file.filename = str(uuid.uuid4()) + file.filename[_dot:]
            filename = secure_filename(file.filename)
            file.save(os.path.normpath(os.path.join(current_app.config["UPLOADED_PATH"], filename)))
            flash("File successfully uploaded")
            return file.filename
        else:
            flash("Not allowed file typed")
            return redirect(request.url)
"""

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

