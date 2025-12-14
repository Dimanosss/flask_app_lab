from flask import Blueprint
import os

# Отримуємо шлях до папки templates блюпринта
template_folder = os.path.join(os.path.dirname(__file__), 'templates', 'products')
products_bp = Blueprint('products', __name__, template_folder=template_folder)

from app.products import views
