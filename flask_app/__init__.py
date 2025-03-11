# my_flask_app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    # Point to your provided database file
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/ausbildung.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'dev'  # Change for production

    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Optionally, comment out create_all if your DB is pre-populated:
    with app.app_context():
        # db.create_all()  # Remove or comment this out if not needed.
        pass

    return app