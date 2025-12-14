# Lab7 - Flask Project з SQLAlchemy та Flask-Migrate

Повний Flask-проект з використанням SQLAlchemy та Flask-Migrate для роботи з базою даних.

## Структура проекту

```
Lab7/
├── app/
│   ├── __init__.py          # Ініціалізація Flask додатку
│   ├── products/            # Блюпринт products
│   │   ├── __init__.py
│   │   ├── models.py        # Моделі Product та Category
│   │   ├── views.py         # Views для products
│   │   └── templates/
│   │       └── products/
│   │           ├── list.html
│   │           └── categories.html
│   ├── templates/
│   │   └── base.html
│   └── migrations/          # Міграції Alembic (створюється після flask db init)
├── run.py                   # Точка входу для запуску додатку
├── requirements.txt         # Залежності проекту
└── README.md               # Цей файл
```

## Встановлення

1. Створіть віртуальне середовище:
```bash
python -m venv venv
```

2. Активуйте віртуальне середовище:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

## Ініціалізація бази даних та міграції

**Важливо**: Моделі вже містять всі поля (id, name, price, active, created_at, category_id). 
Якщо потрібно створити міграції поетапно, див. розділ "Поетапне створення міграцій" нижче.

### Швидкий старт (всі міграції одразу)

1. **Ініціалізація міграцій**:
```bash
flask db init
```

2. **Створення початкової міграції**:
```bash
flask db migrate -m "Initial migration: Add Product and Category models"
flask db upgrade
```

3. **Додавання початкових даних**:
```bash
python init_db.py --data
```

Або через flask shell (див. детальні інструкції нижче).

### Поетапне створення міграцій (згідно з вимогами)

Якщо потрібно створити міграції поетапно, виконайте наступні кроки:

#### Крок 1: Ініціалізація міграцій
```bash
flask db init
```

#### Крок 2: Створення початкової міграції для Product (тільки id, name, price)

Тимчасово закоментуйте поля `active`, `created_at` та `category_id` у `app/products/models.py`, потім:
```bash
flask db migrate -m "Add Product"
flask db upgrade
```

### Крок 3: Додавання початкових даних через flask shell
```bash
flask shell
```

У консолі виконайте:
```python
from app import db
from app.products.models import Product

# Додавання товарів
pc = Product(name="Pc", price=700.0)
mac = Product(name="MAC", price=500.0)

db.session.add(pc)
db.session.add(mac)
db.session.commit()

exit()
```

### Крок 4: Додавання моделі Category та зв'язку
Модель Category вже додана до `models.py`. Створіть міграцію:
```bash
flask db migrate -m "Add Category and relationship with Product"
flask db upgrade
```

### Крок 5: Додавання поля active до Product
Поле `active` вже додане до моделі. Створіть міграцію:
```bash
flask db migrate -m "Add active field to Product"
flask db upgrade
```

### Крок 6: Додавання даних (iPhone 15, Laptops, Gaming Laptop)
```bash
flask shell
```

У консолі:
```python
from app import db
from app.products.models import Product, Category

# Додавання категорії
laptops = Category(name="Laptops")
db.session.add(laptops)
db.session.commit()

# Додавання продуктів
iphone = Product(name="iPhone 15", price=999.99, active=True)
gaming_laptop = Product(name="Gaming Laptop", price=1500.00, active=False, category=laptops)

db.session.add(iphone)
db.session.add(gaming_laptop)
db.session.commit()

# Перевірка зв'язку
print(f"Категорія {laptops.name} має {len(laptops.products)} продуктів")
for product in laptops.products:
    print(f"  - {product.name}")

exit()
```

### Крок 7: Додавання поля created_at
Поле `created_at` вже додане до моделі. Створіть міграцію:
```bash
flask db migrate -m "Add created_at field to Product"
flask db upgrade
```

### Крок 8: Створення порожньої міграції для вставки даних

Якщо `flask db migrate` не бачить змін у схемі, створіть порожню міграцію:
```bash
flask db revision -m "Insert data into products table"
```

Потім відредагуйте файл міграції в `app/migrations/versions/` та додайте вставку даних у функції `upgrade()`:

```python
def upgrade():
    # Вставка даних
    from app.products.models import Product, Category
    from app import db
    
    # Додавання категорії
    laptops = Category(name="Laptops")
    db.session.add(laptops)
    db.session.commit()
    
    # Додавання продуктів
    iphone = Product(name="iPhone 15", price=999.99, active=True, category=None)
    gaming_laptop = Product(name="Gaming Laptop", price=1500.00, active=False, category=laptops)
    
    db.session.add(iphone)
    db.session.add(gaming_laptop)
    db.session.commit()

def downgrade():
    # Видалення даних
    from app.products.models import Product, Category
    from app import db
    
    Product.query.filter(Product.name.in_(["iPhone 15", "Gaming Laptop"])).delete()
    Category.query.filter(Category.name == "Laptops").delete()
    db.session.commit()
```

Потім виконайте:
```bash
flask db upgrade
```

### Крок 9: Перевірка історії міграцій
```bash
flask db history
```

## Запуск додатку

```bash
python run.py
```

Або:
```bash
flask run
```

Додаток буде доступний за адресою: http://127.0.0.1:5000

## Маршрути

- `/` - Головна сторінка
- `/products/` - Список всіх продуктів
- `/products/categories` - Список категорій з продуктами

## Особливості реалізації

1. **Naming Convention**: У `app/__init__.py` налаштовано naming convention для обмежень БД (FK, PK, UQ, etc.)

2. **Моделі**:
   - `Product`: id, name, price, active, created_at, category_id
   - `Category`: id, name
   - Зв'язок 1:N між Category та Product

3. **Міграції**: Використовується Flask-Migrate (Alembic) для керування схемою БД

4. **Шаблони**: Використовується Bootstrap 5 для стилізації

## Примітки

- База даних зберігається в `instance/data.sqlite`
- Всі міграції зберігаються в `app/migrations/versions/`
- Для production змініть `SECRET_KEY` у `app/__init__.py`

