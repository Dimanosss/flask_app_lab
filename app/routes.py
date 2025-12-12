from flask import render_template, request, redirect, url_for, flash, session, make_response
from app import app

VALID_USER = {"username": "admin", "password": "12345"}

@app.route("/")
def home():
    return render_template("base.html", title="Головна")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == VALID_USER["username"] and password == VALID_USER["password"]:
            session["username"] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Невірні дані входу!", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", title="Вхід")

@app.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("login"))
    username = session["username"]
    cookies = request.cookies
    color_scheme = cookies.get("color_scheme", "light")
    return render_template("profile.html", username=username, cookies=cookies, color_scheme=color_scheme)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи!", "info")
    return redirect(url_for("login"))

@app.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("login"))
    key = request.form.get("key")
    value = request.form.get("value")
    resp = make_response(redirect(url_for("profile")))
    if key and value:
        resp.set_cookie(key, value)
        flash(f"Кукі '{key}' додано!", "success")
    else:
        flash("Вкажіть ключ і значення!", "danger")
    return resp

@app.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    key = request.form.get("key")
    resp = make_response(redirect(url_for("profile")))
    if key:
        resp.delete_cookie(key)
        flash(f"Кукі '{key}' видалено!", "info")
    else:
        for k in request.cookies.keys():
            resp.delete_cookie(k)
        flash("Усі кукі видалено!", "info")
    return resp

@app.route("/set_theme/<scheme>")
def set_theme(scheme):
    resp = make_response(redirect(url_for("profile")))
    resp.set_cookie("color_scheme", scheme)
    flash(f"Змінено тему на {scheme}!", "success")
    return resp
