from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response

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


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username in USERS and USERS[username] == password:
            session["username"] = username
            flash("Успішний вхід!", "success")
            return redirect(url_for("users.profile"))
        flash("Wrong data! Try again!", "danger")
        return redirect(url_for("users.login"))
    return render_template("users/login.html", title="Вхід")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Сесія користувача недоступна. Будь ласка, увійдіть.", "warning")
        return redirect(url_for("users.login"))
    username = session.get("username")
    theme = request.cookies.get("theme", "light")
    return render_template("users/profile.html", title="Профіль", username=username, cookies=request.cookies, theme=theme)


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
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
    if "username" not in session:
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
    if "username" not in session:
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
