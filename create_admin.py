# create_admin.py
from models import User, db
from werkzeug.security import generate_password_hash
from app import create_app

app = create_app()

with app.app_context():

    if not User.query.filter_by(email="angelbello9798@gmail.com").first():
        admin = User(
            name="Angel Bello",
            email="angelbello9798@gmail.com",
            password=generate_password_hash("99angelbello9798"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
