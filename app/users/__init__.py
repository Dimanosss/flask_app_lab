from flask import Blueprint
import os

# Отримуємо шлях до папки templates блюпринта
template_folder = os.path.join(os.path.dirname(__file__), 'templates', 'users')
users_bp = Blueprint('users', __name__, template_folder=template_folder)

from app.users import views
