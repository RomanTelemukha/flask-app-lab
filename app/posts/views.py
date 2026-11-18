from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, abort
from .. import db
from . import post_bp
from .models import Post
from .forms import PostForm


@post_bp.route("/create", methods=["GET", "POST"])
@post_bp.route("/add_post", methods=["GET", "POST"], endpoint="add_post")
def create_post():
    form = PostForm()
    if request.method == "POST":
        if not form.content.data and request.form.get("text"):
            form.content.data = request.form.get("text")
    if form.validate_on_submit():
        author = session.get("username", "Anonymous")
        publish_date = form.publish_date.data or datetime.utcnow()
        new_post = Post(
            title=form.title.data,
            content=form.content.data or "",
            is_active=form.is_active.data,
            posted=publish_date,
            category=form.category.data,
            author=author
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.post_list"))
    return render_template("add_post.html", form=form, title="Create a New Post")


@post_bp.route("", methods=["GET"])
@post_bp.route("/", methods=["GET"])
@post_bp.route("/all", methods=["GET"], endpoint="all_posts")
@post_bp.route("/posts", methods=["GET"], endpoint="get_posts")
def post_list():
    stmt = db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/<int:id>", methods=["GET"])
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
@post_bp.route("/<int:id>/edit", methods=["GET", "POST"], endpoint="edit_post")
@post_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if request.method == "GET":
        form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data or request.form.get("text", post.content)
        post.is_active = form.is_active.data
        if form.publish_date.data:
            post.posted = form.publish_date.data
        post.category = form.category.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    return render_template("add_post.html", form=form, post=post, is_edit=True, title="Редагувати пост")


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
@post_bp.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалено.", "danger")
        return redirect(url_for("posts.post_list"))
    return render_template("delete_confirm.html", post=post)
