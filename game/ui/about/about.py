from flask import Blueprint, render_template, request

from game.core.constants import USER_IDENTIFIER


about_blueprint = Blueprint('about_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/ui/about')


@about_blueprint.route("/about")
def about_window():
    """
    The function which is mapped to `/about` and handles its logic
    """

    if USER_IDENTIFIER in request.cookies:
        if request.cookies[USER_IDENTIFIER] != "logged-out":
            user_identified = True
        else:
            user_identified = False
    
    else:
        user_identified = False

    return render_template("about-window.html", user_identified=user_identified)
