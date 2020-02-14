from flask import Blueprint


api_blueprint = Blueprint(__name__, url_prefix="api/")


@api_blueprint.get("auth/login/")
def auth():
    pass


@api_blueprint.post("disk-statictics/")
def disk_statistics():
    pass


@api_blueprint.get("disk-statictics/")
def get_disk_statistics():
    pass
