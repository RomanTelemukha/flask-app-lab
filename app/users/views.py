from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from .models import User
from .forms import RegistrationForm, LoginForm

users_bp = Blueprint("users", __name__, template_folder="templates")

USERS = {
    "admin": "admin123",
    "user1": "password"
}

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    return redirect(to_url)

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("users.login"))
    return render_template("users/register.html", form=form, title="Register")

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))
    form = LoginForm()
    if form.validate_on_submit():
        ident = form.username.data or form.email.data
        password = form.password.data
        user = User.query.filter((User.username == ident) | (User.email == ident)).first()
        if user and user.check_password(password):
            login_user(user, remember=form.remember.data)
            session["username"] = user.username
            flash("You logged in successfully!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("users.account"))
        if ident in USERS and USERS[ident] == password:
            user = User.query.filter_by(username=ident).first()
            if not user:
                user = User(username=ident, email=f"{ident}@example.com", password=password)
                user.hash_password()
                db.session.add(user)
                db.session.commit()
            login_user(user, remember=form.remember.data)
            session["username"] = user.username
            flash("You logged in successfully!", "success")
            return redirect(url_for("users.account"))
        flash("Wrong data! Try again! Error: Invalid username or password.", "danger")
    elif request.method == "POST":
        ident = request.form.get("username", "").strip() or request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        if ident and password:
            user = User.query.filter((User.username == ident) | (User.email == ident)).first()
            if (user and user.check_password(password)) or (ident in USERS and USERS[ident] == password):
                if not user:
                    user = User(username=ident, email=f"{ident}@example.com", password=password)
                    user.hash_password()
                    db.session.add(user)
                    db.session.commit()
                login_user(user, remember=False)
                session["username"] = user.username
                flash("You logged in successfully!", "success")
                return redirect(url_for("users.account"))
            flash("Wrong data! Try again! Error: Invalid username or password.", "danger")
    return render_template("users/login.html", form=form, title="Login")

@users_bp.route("/account")
@login_required
def account():
    return render_template("users/account.html", user=current_user, title="Account")

@users_bp.route("/users_list")
@users_bp.route("/users")
@login_required
def users_list():
    users = User.query.all()
    count = len(users)
    return render_template("users/users_list.html", users=users, count=count, title="Users List")

@users_bp.route("/logout")
def logout():
    logout_user()
    session.pop("username", None)
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/profile")
def profile():
    if "username" not in session and not current_user.is_authenticated:
        flash("Сесія користувача недоступна. Будь ласка, увійдіть.", "warning")
        return redirect(url_for("users.login"))
    username = current_user.username if current_user.is_authenticated else session.get("username")
    theme = request.cookies.get("theme", "light")
    return render_template("users/profile.html", title="Профіль", username=username, cookies=request.cookies, theme=theme)

@users_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
    if "username" not in session and not current_user.is_authenticated:
        flash("Сесія недоступна.", "warning")
        return redirect(url_for("users.login"))
    key = request.form.get("cookie_key", "").strip()
    value = request.form.get("cookie_value", "").strip()
    expire = request.form.get("cookie_expire", "").strip()
    response = make_response(redirect(url_for("users.profile")))
    if key:
        max_age = int(expire) if expire and expire.isdigit() else None
        response.set_cookie(key, value, max_age=max_age)
        flash(f"Кукі '{key}' успішно додано!", "success")
    else:
        flash("Ключ кукі не може бути порожнім!", "danger")
    return response

@users_bp.route("/cookie/delete", methods=["POST"])
def delete_cookie():
    if "username" not in session and not current_user.is_authenticated:
        flash("Сесія недоступна.", "warning")
        return redirect(url_for("users.login"))
    key = request.form.get("delete_key", "").strip()
    response = make_response(redirect(url_for("users.profile")))
    if key:
        response.delete_cookie(key)
        flash(f"Кукі '{key}' успішно видалено!", "info")
    else:
        flash("Вкажіть ключ для видалення!", "danger")
    return response

@users_bp.route("/cookie/delete_all", methods=["POST"])
def delete_all_cookies():
    if "username" not in session and not current_user.is_authenticated:
        flash("Сесія недоступна.", "warning")
        return redirect(url_for("users.login"))
    response = make_response(redirect(url_for("users.profile")))
    for key in list(request.cookies.keys()):
        if key != "session":
            response.delete_cookie(key)
    flash("Всі кукі успішно видалено!", "info")
    return response

@users_bp.route("/theme/<string:theme_name>")
def change_theme(theme_name):
    response = make_response(redirect(url_for("users.profile")))
    if theme_name in ["light", "dark"]:
        response.set_cookie("theme", theme_name, max_age=30 * 24 * 60 * 60)
        flash(f"Кольорову схему змінено на {theme_name}!", "info")
    return response
