from flask import Flask

from os_cleaner.api.views import init_api
from os_cleaner.db import init_db


def create_app(settings: str = "local") -> Flask:
    app = Flask(__name__)
    register_extensions(app)
    return app


def register_extensions(app: Flask) -> None:
    init_db(app)
    init_api(app)
