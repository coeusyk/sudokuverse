from flask import Blueprint, render_template


play_window_blueprint = Blueprint("play_window_blueprint", __name__, template_folder="templates", static_folder="static")


@play_window_blueprint.route("/play")
def play_window():
    return render_template("play-window.html")
