from flask import Blueprint, render_template, request

from game.core.constants import USER_IDENTIFIER


learn_blueprint = Blueprint("learn_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/learn")


@learn_blueprint.route("/how-to-play", methods=["GET"])
def how_to_play_window():
    if USER_IDENTIFIER in request.cookies:
        if request.cookies[USER_IDENTIFIER] != "logged-out":
            user_identified = True
        else:
            user_identified = False
    
    else:
        user_identified = False

    return render_template("learn-window.html", user_identified=user_identified)
