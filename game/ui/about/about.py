from flask import Blueprint, render_template


about_blueprint = Blueprint('about_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/ui/about')


@about_blueprint.route("/about")
def about_window():
    return render_template("about-window.html")
