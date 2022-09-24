from flask import Blueprint, render_template


ranks_blueprint = Blueprint('ranks_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/ui/ranks')


@ranks_blueprint.route("/leaderboard")
def leaderboard_window():
    return render_template("leaderboard-window.html")
