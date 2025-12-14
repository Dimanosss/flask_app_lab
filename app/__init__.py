from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Реєстрація блюпринтів
    from app.users import users_bp
    from app.products import products_bp
    
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    
    # Реєстрація роутів, що не належать блюпринтам
    from app import views
    views.register_routes(app)
    
    return app

app = create_app()
