from flask import render_template
from ui.play import play_blueprint


@play_blueprint.route("/play")
def play_window():
    return render_template("play-window.html")
