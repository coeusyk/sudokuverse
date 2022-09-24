from flask import Blueprint, render_template


main_blueprint = Blueprint("main_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/main")


@main_blueprint.route("/main")
def main_window():
    return render_template("grid.html")
