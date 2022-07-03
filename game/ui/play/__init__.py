from flask import Blueprint


play_blueprint = Blueprint("play_blueprint", __name__, template_folder="templates", static_folder="static")
