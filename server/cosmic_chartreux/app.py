from flask import Flask


def create_app(settings: str = "local") -> Flask:
    app = Flask(__name__)
    app.config
    return app
