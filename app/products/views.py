import os
import uuid
from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from .forms import ProductForm
from .db import get_all_products, get_product_by_id, insert_product, update_product, delete_product

products_bp = Blueprint("products", __name__, template_folder="templates")


def save_product_image(image_file):
    if not image_file or not getattr(image_file, "filename", None):
        return ""
    ext = os.path.splitext(secure_filename(image_file.filename))[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    upload_dir = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    image_file.save(os.path.join(upload_dir, filename))
    return f"uploads/{filename}"


@products_bp.route("")
@products_bp.route("/")
def product_list():
    products = get_all_products()
    return render_template("products/products.html", products=products)


@products_bp.route("/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = save_product_image(form.image.data)
        product_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": int(form.quantity.data),
            "image": image_path
        }
        insert_product(product_data)
        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.product_list"))
    return render_template("products/add_product.html", form=form)


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if product is None:
        abort(404)
    return render_template("products/detail_product.html", product=product)


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = get_product_by_id(product_id)
    if product is None:
        abort(404)
    form = ProductForm()
    if form.validate_on_submit():
        image_path = product.get("image", "")
        if form.image.data and getattr(form.image.data, "filename", None):
            image_path = save_product_image(form.image.data)
        update_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": int(form.quantity.data),
            "image": image_path
        }
        update_product(product_id, update_data)
        flash("Товар успішно оновлено!", "success")
        return redirect(url_for("products.product_detail", product_id=product_id))
    elif request.method == "GET":
        form.name.data = product.get("name", "")
        form.content.data = product.get("content", "")
        form.price.data = product.get("price", 0.0)
        form.category.data = product.get("category", "")
        form.quantity.data = product.get("quantity", 0)
    return render_template("products/edit_product.html", form=form, product=product)


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    product = get_product_by_id(product_id)
    if product is None:
        abort(404)
    delete_product(product_id)
    flash("Товар успішно видалено!", "info")
    return redirect(url_for("products.product_list"))
