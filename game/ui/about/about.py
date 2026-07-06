from flask import Blueprint, render_template

from game.core.auth import is_logged_in


about_blueprint = Blueprint('about_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/ui/about')


@about_blueprint.route("/about")
def about_window():
    """
    The function which is mapped to `/about` and handles its logic
    """

    return render_template("about-window.html", user_identified=is_logged_in())
