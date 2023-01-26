from flask import Blueprint, render_template


stats_blueprint = Blueprint('stats_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/ui/stats')


@stats_blueprint.route("/profile/<username>")
def personal_profile_window(username: str):
    return render_template("profile-window.html")
