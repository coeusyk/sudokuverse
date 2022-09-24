from flask import Blueprint, render_template


learn_blueprint = Blueprint('learn_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/ui/learn')


@learn_blueprint.route("/how-to-play")
def how_to_play_window():
    return render_template("howToPlay-window.html")
