from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registrar rutas
    with app.app_context():
        from . import routes
        return app
