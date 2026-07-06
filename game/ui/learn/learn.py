from flask import Blueprint, render_template

from game.core.auth import is_logged_in


learn_blueprint = Blueprint("learn_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/learn")


@learn_blueprint.route("/how-to-play", methods=["GET"])
def how_to_play_window():
    return render_template("learn-window.html", user_identified=is_logged_in())
