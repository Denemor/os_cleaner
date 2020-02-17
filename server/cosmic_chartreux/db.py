from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask) -> None:
    db.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"

    with app.app_context():
        # Remove after test
        db.drop_all()
        db.create_all()
