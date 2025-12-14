"""
Скрипт для ініціалізації бази даних та додавання початкових даних.
Використовується для автоматизації процесу налаштування проекту.
"""
import os
import sys
from app import create_app, db
from app.products.models import Product, Category

def init_database():
    """Ініціалізація бази даних та створення таблиць"""
    app = create_app()
    with app.app_context():
        # Створення всіх таблиць
        db.create_all()
        print("✓ Таблиці створено успішно")

def add_initial_data():
    """Додавання початкових даних"""
    app = create_app()
    with app.app_context():
        # Перевірка, чи вже є дані
        if Product.query.count() > 0:
            print("⚠ Дані вже існують у базі. Пропускаю додавання початкових даних.")
            return
        
        # Додавання товарів (Частина 1)
        print("Додаю початкові товари...")
        pc = Product(name="Pc", price=700.0, active=True)
        mac = Product(name="MAC", price=500.0, active=True)
        db.session.add(pc)
        db.session.add(mac)
        db.session.commit()
        print("✓ Додано: Pc (700), MAC (500)")
        
        # Додавання категорії та продуктів (Частина 5)
        print("Додаю категорію та продукти...")
        laptops = Category(name="Laptops")
        db.session.add(laptops)
        db.session.commit()
        
        iphone = Product(name="iPhone 15", price=999.99, active=True)
        gaming_laptop = Product(name="Gaming Laptop", price=1500.00, active=False, category=laptops)
        
        db.session.add(iphone)
        db.session.add(gaming_laptop)
        db.session.commit()
        print("✓ Додано: iPhone 15 (999.99)")
        print("✓ Додано: Gaming Laptop (1500.00, active=False, category=Laptops)")
        print("✓ Додано категорію: Laptops")
        
        # Перевірка зв'язку
        print(f"\n✓ Перевірка: Категорія '{laptops.name}' має {len(laptops.products)} продуктів")
        for product in laptops.products:
            print(f"  - {product.name}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        init_database()
    elif len(sys.argv) > 1 and sys.argv[1] == '--data':
        add_initial_data()
    else:
        print("Використання:")
        print("  python init_db.py --init  # Створити таблиці")
        print("  python init_db.py --data  # Додати початкові дані")

