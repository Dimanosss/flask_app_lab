import logging
from pathlib import Path
from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.forms import ContactForm, LoginForm

VALID_USER = {"username": "admin", "password": "1234"}

contact_logger = logging.getLogger("contact")
if not contact_logger.handlers:
    Path("logs").mkdir(exist_ok=True)
    fh = logging.FileHandler("logs/contact.log", encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    contact_logger.addHandler(fh)
    contact_logger.setLevel(logging.INFO)

@app.route("/")
def home():
    return render_template("base.html", title="Головна")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip()
        message = form.message.data.strip()

        try:
            contact_logger.info("Contact form: name=%s, email=%s, msg_len=%d", name, email, len(message))
            flash(f"✅ Повідомлення надіслано успішно для {name} <{email}>.", "success")
            session["last_contact"] = {"name": name, "email": email, "message": message}
        except Exception as e:
            app.logger.exception("Помилка запису у лог: %s", e)
            flash("❌ Сталася помилка при записі повідомлення. Спробуйте ще раз.", "danger")

        return redirect(url_for("contact"))

    last = session.get("last_contact")
    return render_template("contact.html", title="Контакти", form=form, last=last)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        remember = form.remember.data

        # Збережемо останні введені поля (вимога 8** — показ таблиці на сторінці)
        session["last_login"] = {"username": username, "remember": "так" if remember else "ні"}

        if username == VALID_USER["username"] and password == VALID_USER["password"]:
            session["username"] = username
            extra = " (опція 'Запам'ятати' увімкнена)" if remember else ""
            flash(f"🔐 Успішний вхід як {username}{extra}.", "success")
            return redirect(url_for("profile"))
        else:
            flash("❌ Невірні дані автентифікації.", "danger")
            return redirect(url_for("login"))  # PRG після невдалого логіну

    # GET або невалідний POST (помилки валідації показуються поряд із полями)
    last_login = session.get("last_login")
    return render_template("login.html", title="Вхід", form=form, last=last_login)

@app.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку виконайте вхід.", "warning")
        return redirect(url_for("login"))
    return render_template("profile.html", title="Профіль", username=session["username"])

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("login"))
