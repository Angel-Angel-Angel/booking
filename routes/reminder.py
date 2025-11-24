from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User
from routes.auth import auth_bp
from routes.bookings import bookings_bp
from routes.main import main_bp
import os


def create_app():
    app = Flask(__name__)


    app.config["SECRET_KEY"] = "super_secret_key_change_this"


    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")


    with app.app_context():
        if not os.path.exists("instance"):
            os.mkdir("instance")
        db_path = os.path.join("instance", "app.db")
        if not os.path.exists(db_path):
            db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
