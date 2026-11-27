from app.users.models import User
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, abort
from .. import db
from . import post_bp
from .models import Post, Tag
from .forms import PostForm


@post_bp.route("/create", methods=["GET", "POST"])
@post_bp.route("/add_post", methods=["GET", "POST"], endpoint="add_post")
def create_post():
    form = PostForm()

    authors = db.session.scalars(db.select(User)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    all_tags = db.session.scalars(db.select(Tag)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in all_tags]

    if request.method == "POST":
        if not form.content.data and request.form.get("text"):
            form.content.data = request.form.get("text")

    if form.validate_on_submit():
        publish_date = form.publish_date.data or datetime.utcnow()
        selected_tags = db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
        new_post = Post(
            title=form.title.data,
            content=form.content.data or "",
            is_active=form.is_active.data,
            posted=publish_date,
            category=form.category.data,
            user_id=form.author_id.data,
            tags=selected_tags
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
    form = PostForm(
        title=post.title,
        content=post.content,
        is_active=post.is_active,
        publish_date=post.posted,
        category=post.category,
        author_id=post.user_id,
        tags=[tag.id for tag in post.tags]
    )

    authors = db.session.scalars(db.select(User)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    all_tags = db.session.scalars(db.select(Tag)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in all_tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data or request.form.get("text", post.content)
        post.is_active = form.is_active.data
        if form.publish_date.data:
            post.posted = form.publish_date.data
        post.category = form.category.data
        post.user_id = form.author_id.data
        post.tags = db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
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