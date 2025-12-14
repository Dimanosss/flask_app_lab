from flask import render_template
from app.products import products_bp

@products_bp.route('/')
def list_products():
    """Список продуктів"""
    products = [
        {'id': 1, 'name': 'Ноутбук', 'price': 25000, 'description': 'Потужний ноутбук для роботи'},
        {'id': 2, 'name': 'Смартфон', 'price': 15000, 'description': 'Сучасний смартфон з відмінною камерою'},
        {'id': 3, 'name': 'Планшет', 'price': 12000, 'description': 'Легкий та зручний планшет'},
    ]
    return render_template('list.html', products=products, title="Продукти")

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Деталі продукту"""
    # Симуляція отримання продукту з бази даних
    products = {
        1: {'id': 1, 'name': 'Ноутбук', 'price': 25000, 'description': 'Потужний ноутбук для роботи', 'specs': 'Intel i7, 16GB RAM, 512GB SSD'},
        2: {'id': 2, 'name': 'Смартфон', 'price': 15000, 'description': 'Сучасний смартфон з відмінною камерою', 'specs': '6.5", 128GB, 48MP камера'},
        3: {'id': 3, 'name': 'Планшет', 'price': 12000, 'description': 'Легкий та зручний планшет', 'specs': '10.1", 64GB, Wi-Fi'},
    }
    product = products.get(product_id)
    if not product:
        return render_template('404.html', title="Продукт не знайдено"), 404
    return render_template('detail.html', product=product, title=product['name'])
