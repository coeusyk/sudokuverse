import json
import datetime
import uuid

from flask import Blueprint, render_template, request, Response, redirect, url_for

from game.models import db, User, GameStats
from game.core.constants import CELL_ATTRIBUTES
from game.core.partial_creator import create_puzzle
from game.core.solver import get_solution
from game.core.constants import USER_IDENTIFIER, DIFFICULTY_DICT, DIFF_CHOSEN, NUMBERS
from game.core.stats_functionalities import convert_timer_value


gameplay_blueprint = Blueprint("gameplay_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/gameplay")


@gameplay_blueprint.route("/gameplay", methods=["GET", "POST"])
def gameplay_window():
    # Checking if the request sent was valid or not:
    if DIFF_CHOSEN in request.cookies:
        # Giving an advantage for signed-in users (increased number of hints):
        if USER_IDENTIFIER in request.cookies:
            max_hints = 5
        else:
            max_hints = 3

    else:
        if USER_IDENTIFIER in request.cookies:
            return redirect(url_for('home_blueprint.home_window'))
        else:
            return redirect(url_for('play_blueprint.play_window'))


    if request.method == "POST":
        if request.headers['Content-Type'] == "application/json":
            game_stats: dict = request.get_json()

            user_record = User.query.filter_by(uid=request.cookies[USER_IDENTIFIER]).first()

            end_time = datetime.datetime.now()

            if game_stats["time-taken"] is not None:
                start_time = end_time - convert_timer_value(game_stats["time-taken"])
            else:
                start_time = None
                end_time = None

            entry_id = str(uuid.uuid1())

            stats_record = GameStats(
                entry_id=entry_id,
                uid=user_record.uid,
                start_time=start_time,
                end_time=end_time,
                hints_used=game_stats["hints-used"],
                game_result=game_stats["game-result"],
                game_type=DIFFICULTY_DICT[game_stats["difficulty"]]
            )

            db.session.add(stats_record)
            db.session.commit()

            info_added_resp = Response(json.dumps({"info-added": True}), status=302)

            return info_added_resp
        
        else:
            global difficulty, diff_id, solution, partial_board

            difficulty = request.form.get("difficulty")
            diff_id = DIFFICULTY_DICT[difficulty]

            solution = get_solution()
            partial_board = create_puzzle(solution, difficulty=diff_id)

            # Returning a response:
            new_game_resp = Response(status=205)
            
            return new_game_resp
    
    if request.method == "GET":
        try:
            if solution:
                pass

        except NameError:
            diff_id = int(request.cookies[DIFF_CHOSEN])

            difficulty = list(filter(lambda key: DIFFICULTY_DICT[key] == diff_id, DIFFICULTY_DICT))[0]
            
            solution = get_solution()
            partial_board = create_puzzle(solution, difficulty=diff_id)


    return render_template(
        "gameplay-window.html", 
        cell_attributes = CELL_ATTRIBUTES, 
        partial = partial_board, 
        difficulty = difficulty.capitalize(), 
        nums = NUMBERS, 
        solution = solution,
        max_hints = max_hints
    )
