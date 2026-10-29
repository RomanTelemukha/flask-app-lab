from flask import request, redirect, url_for, render_template, abort
from app import app


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


@app.route("/contacts")
def contacts():
    return render_template("contacts.html", title="Контакти")


@app.route("/login")
def login_redirect():
    return redirect(url_for("users.login"))


@app.route("/profile")
def profile_redirect():
    return redirect(url_for("users.profile"))
