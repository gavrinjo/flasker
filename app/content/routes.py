from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.content import bp, handlers
from app.content.forms import PostForm, EditPostForm
from app.models import Post


@bp.route("/postit", methods=["GET", "POST"])
@login_required
def postit():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=handlers.img_proc(form.post.data), author=current_user)
        # print(post)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!!")
        return redirect(url_for("main.index"))
    return render_template("postit.html", title="Post Content", form=form)


@bp.route("/edit_page/<id>", methods=["GET", "POST"])
@login_required
def edit_page(id):
    form = EditPostForm()
    if form.validate_on_submit():
        if form.submit.data:
            return redirect(url_for("submit"))
        elif form.cancel.data:
            return redirect(url_for("cancel"))
    #if request.method == "POST":
        #post = Post.query.filter_by(id=id)

    return render_template("edit_page.html", title="Edit Post Content", form=form)