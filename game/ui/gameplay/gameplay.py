from flask import Blueprint, render_template

from game.core.constants import CELL_ATTRIBUTES
from game.core.partial_creator import partial_board


gameplay_blueprint = Blueprint("gameplay_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/gameplay")


@gameplay_blueprint.route("/gameplay")
def gameplay_window():
    return render_template("grid.html", cell_attributes=CELL_ATTRIBUTES, partial=partial_board)
