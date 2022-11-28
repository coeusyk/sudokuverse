from flask import Blueprint, render_template

from game.core.constants import CELL_ATTRIBUTES
from game.core.partial_creator import create_partial
from game.core.solver import get_solution


gameplay_blueprint = Blueprint("gameplay_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/gameplay")


@gameplay_blueprint.route("/gameplay")
def gameplay_window():
    diff = 1 
    diff_names = ("Simple", "Medium", "Complex")
    solution = get_solution()

    partial_board = create_partial(solution, difficulty=diff)
    
    return render_template("gameplay-window.html", cell_attributes=CELL_ATTRIBUTES, partial=partial_board, difficulty=diff_names[diff - 1], nums=range(1, 10), 
                            solution=solution)
