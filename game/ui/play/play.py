import json

from flask import Blueprint, render_template, request, redirect, url_for, Response
from game.core.constants import USER_IDENTIFIER, DIFFICULTY_DICT, DIFF_CHOSEN, SIMPLE, MEDIUM, COMPLEX

play_blueprint = Blueprint("play_blueprint", __name__, template_folder="templates", static_folder="static",
                           static_url_path="/ui/play")


@play_blueprint.route("/play", methods=['GET', 'POST'])
def play_window():
    if USER_IDENTIFIER in request.cookies:
        if request.cookies[USER_IDENTIFIER] != "logged-out":
            return redirect(url_for('home_blueprint.home_window'), code=302)

    if request.method == "POST":
        difficulty = request.form.get("difficulty")
        diff_id = DIFFICULTY_DICT[difficulty]

        difficulty_response = redirect(url_for('gameplay_blueprint.gameplay_window'), code=302)
        difficulty_response.set_cookie(DIFF_CHOSEN, str(diff_id))

        return difficulty_response

    return render_template(
        "play-window.html",

        simple_min=SIMPLE[0], simple_max=SIMPLE[-1],
        medium_min=MEDIUM[0], medium_max=MEDIUM[-1],
        complex_min=COMPLEX[0], complex_max=COMPLEX[-1]
    )
