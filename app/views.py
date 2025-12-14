from flask import render_template

def register_routes(app):
    """Реєстрація роутів, що не належать блюпринтам"""
    @app.route('/')
    def index():
        """Головна сторінка"""
        return render_template('index.html', title="Головна")

    @app.route('/about')
    def about():
        """Сторінка про проект"""
        return render_template('about.html', title="Про проект")

