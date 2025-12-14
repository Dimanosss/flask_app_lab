from flask import render_template
from app.users import users_bp

@users_bp.route('/hi/<name>')
def hi(name):
    """Привітання користувача"""
    return render_template('hi.html', name=name, title=f"Привіт, {name}!")

@users_bp.route('/admin')
def admin():
    """Адміністративна панель"""
    return render_template('admin.html', title="Адмін панель")
