from flask import render_template
from app.products import products_bp
from app.products.models import Product, Category
from app import db
from sqlalchemy import select

@products_bp.route('/')
def list_products():
    """Список всіх продуктів"""
    stmt = select(Product).order_by(Product.id)
    products = db.session.scalars(stmt).all()
    return render_template('products/list.html', products=products, title="Продукти")

@products_bp.route('/categories')
def list_categories():
    """Список всіх категорій з продуктами"""
    stmt = select(Category).order_by(Category.id)
    categories = db.session.scalars(stmt).all()
    return render_template('products/categories.html', categories=categories, title="Категорії")

