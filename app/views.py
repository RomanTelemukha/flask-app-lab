import os
import logging
from flask import request, redirect, url_for, render_template, abort, flash
from app import app
from app.forms import ContactForm

log_file_path = os.path.join(os.path.dirname(app.root_path), "feedback.log")
logger = logging.getLogger("contacts")
logger.setLevel(logging.INFO)
if not logger.handlers:
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


@app.route("/")
def main():
    return render_template("index.html", title="Головна")


@app.route("/homepage")
def home():
    agent = request.user_agent
    return render_template("homepage.html", title="Homepage", agent=agent)


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contact", methods=["GET", "POST"])
@app.route("/contacts", methods=["GET", "POST"], endpoint="contacts")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        logger.info(
            f"Contact Form: name={form.name.data}, email={form.email.data}, phone={form.phone.data}, subject={form.subject.data}, message={form.message.data}"
        )
        flash("Повідомлення успішно надіслано та збережено!", "success")
        return redirect(url_for("contact"))
    elif request.method == "POST":
        logger.warning(f"Contact Form validation failed: {form.errors}")
        flash("Помилка при заповненні форми. Перевірте введені дані.", "danger")
    return render_template("contacts.html", title="Контакти", form=form)


@app.route("/login")
def login_redirect():
    return redirect(url_for("users.login"))


@app.route("/profile")
def profile_redirect():
    return redirect(url_for("users.profile"))
