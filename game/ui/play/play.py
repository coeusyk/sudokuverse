from flask import Blueprint, render_template

from game.core.constants import CELL_ATTRIBUTES


play_blueprint = Blueprint("play_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/play")


@play_blueprint.route("/play")
def play_window():
    return render_template("play-window.html", cell_attributes=CELL_ATTRIBUTES)
