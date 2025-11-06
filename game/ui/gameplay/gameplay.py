import json
import datetime
import uuid

from flask import Blueprint, render_template, request, Response, redirect, url_for, session

from game.models import db, User, GameStats
from game.core.constants import CELL_ATTRIBUTES
from game.core.partial_creator import create_puzzle
from game.core.solver import get_solution
from game.core.constants import USER_IDENTIFIER, DIFFICULTY_DICT, DIFF_CHOSEN, NUMBERS
from game.core.stats_functionalities import convert_timer_value, get_timer_value


gameplay_blueprint = Blueprint("gameplay_blueprint", __name__, template_folder="templates", static_folder="static",
                               static_url_path="/ui/gameplay")


@gameplay_blueprint.route("/gameplay/clear-session", methods=["POST"])
def clear_gameplay_session():
    """Clear the current puzzle from session"""
    session.pop('current_puzzle', None)
    return Response(json.dumps({"cleared": True}), status=200)


@gameplay_blueprint.route("/gameplay", methods=["GET", "POST"])
def gameplay_window():
    # Checking if the request sent was valid or not:
    if DIFF_CHOSEN in request.cookies:
        # Giving an advantage for signed in users (increased number of hints):
        if (USER_IDENTIFIER in request.cookies) and (request.cookies[USER_IDENTIFIER] != "logged-out"):
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
            
            # If user quit (game_result == 0), clear the session puzzle
            if game_stats["game-result"] == 0:
                session.pop('current_puzzle', None)

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

            response_data = {"info-added": True}
            
            # If game was completed, get best time for this difficulty
            if game_stats["game-result"] == 1 and game_stats["time-taken"] is not None:
                # Get all completed games for this difficulty
                completed_games = GameStats.query.filter_by(
                    uid=user_record.uid,
                    game_type=DIFFICULTY_DICT[game_stats["difficulty"]],
                    game_result=1
                ).all()
                
                if len(completed_games) > 0:
                    # Find the fastest time
                    fastest_timedelta = None
                    for record in completed_games:
                        if record.start_time and record.end_time:
                            time_delta = record.end_time - record.start_time
                            if fastest_timedelta is None or time_delta < fastest_timedelta:
                                fastest_timedelta = time_delta
                    
                    if fastest_timedelta:
                        best_time_str = get_timer_value(fastest_timedelta)
                        response_data["best-time"] = best_time_str

            info_added_resp = Response(json.dumps(response_data), status=200)

            return info_added_resp

        elif request.headers['Content-Type'] == "application/x-www-form-urlencoded":
            difficulty = request.form.get("difficulty")
            diff_id = DIFFICULTY_DICT[difficulty]

            # Generate new puzzle and store in session
            solution = get_solution()
            partial_board = create_puzzle(solution, difficulty=diff_id)
            
            # Store puzzle in session so refresh doesn't regenerate
            session['current_puzzle'] = {
                'solution': solution,
                'partial': partial_board,
                'difficulty': difficulty,
                'diff_id': diff_id
            }

            # Returning a response:
            new_game_resp = Response(status=205)

            return new_game_resp

    if request.method == "GET":
        diff_id = int(request.cookies[DIFF_CHOSEN])
        difficulty = list(filter(lambda key: DIFFICULTY_DICT[key] == diff_id, DIFFICULTY_DICT))[0]
        
        # Check if we have a puzzle in session for this difficulty
        if 'current_puzzle' in session and session['current_puzzle']['diff_id'] == diff_id:
            # Use existing puzzle from session
            solution = session['current_puzzle']['solution']
            partial_board = session['current_puzzle']['partial']
        else:
            # Generate new puzzle and store in session
            solution = get_solution()
            partial_board = create_puzzle(solution, difficulty=diff_id)
            
            session['current_puzzle'] = {
                'solution': solution,
                'partial': partial_board,
                'difficulty': difficulty,
                'diff_id': diff_id
            }

    return render_template(
        "gameplay-window.html",
        cell_attributes=CELL_ATTRIBUTES,
        partial=partial_board,
        difficulty=difficulty.capitalize(),
        nums=NUMBERS,
        solution=solution,
        max_hints=max_hints
    )
