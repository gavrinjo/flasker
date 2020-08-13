from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.content import bp, handlers
from app.content.forms import PostForm, EditPostForm
from app.models import Post
from sqlalchemy.orm.attributes import flag_modified


@bp.route("/postit", methods=["GET", "POST"])
@login_required
def postit():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, subtitle=form.subtitle.data, body=handlers.img_proc(form.post.data), author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!!")
        return redirect(url_for("main.index"))
    return render_template("postit.html", title="Post Content", form=form)


@bp.route("/<title>", methods=["GET", "POST"])
# @login_required
def page_view(title):
    post = Post.query.filter_by(title=title).first_or_404()
    return render_template("page_view.html", title=post.title, post=post, author=post.author.username)


@bp.route("/edit_page/<id>", methods=["GET", "POST"])
@login_required
def edit_page(id=None):
    form = EditPostForm()
    post = Post.query.get(id)
    if form.validate_on_submit():
        if request.form.get("cancel"):
            return redirect(url_for("main.index"))
        else:
            post.title = form.title.data
            post.subtitle = form.subtitle.data
            post.body = handlers.img_proc(form.post.data)
            db.session.commit()
            flash("You have edited post successfully!!")
            return redirect(url_for("main.index"))
    elif request.method == "GET":
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.post.data = post.body
    return render_template("edit_page.html", title="Edit Post Content", form=form)


@bp.route("/delete_page/<id>", methods=["GET", "POST"])
@login_required
def delete_page(id=None):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("main.index"))


