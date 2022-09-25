from flask import Blueprint, render_template


stats_blueprint = Blueprint('stats_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/ui/stats')


@stats_blueprint.route("/personal-profile")
def personal_profile_window():
    return render_template("personalProfile-window.html")
