import json

from flask import Blueprint, render_template, session, abort

from game.core.constants import CELL_ATTRIBUTES
from game.core.partial_creator import create_partial
from game.core.solver import get_solution


gameplay_blueprint = Blueprint("gameplay_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/gameplay")


@gameplay_blueprint.route("/gameplay", methods=["GET", "POST"])
def gameplay_window():
    difficulty_dict = {"SIMPLE": 1, "MEDIUM": 2, "COMPLEX": 3}
    solution = get_solution()

    # Checking if the request sent was valid or not:
    if session.get('game-info') is None:
        abort(404)
    else:
        game_info: dict = json.loads(session['game-info'])

        difficulty: str = game_info['difficulty']
        diff_id = difficulty_dict[difficulty]

        difficulty = difficulty.capitalize()
        
    partial_board = create_partial(solution, difficulty=diff_id)

    return render_template(
        "gameplay-window.html", 
        cell_attributes=CELL_ATTRIBUTES, 
        partial=partial_board, 
        difficulty=difficulty, 
        nums=range(1, 10), 
        solution=solution
    )
