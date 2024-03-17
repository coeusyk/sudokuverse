import datetime
import json

from flask import Blueprint, render_template, request, redirect, url_for, make_response

from game.models import User, GameStats
from game.core.constants import USER_IDENTIFIER, NUM_OF_DIFFICULTIES, DIFFICULTY_DICT, DIFF_CHOSEN, \
    DIFF_RESP, SIMPLE, MEDIUM, COMPLEX
from game.core.stats_functionalities import format_datetime, get_fastest_time, get_games_per_diff, get_timer_value

home_blueprint = Blueprint("home_blueprint", __name__, template_folder="templates", static_folder="static",
                           static_url_path="/ui/home")


@home_blueprint.route("/home", methods=["GET", "POST"])
def home_window():
    if USER_IDENTIFIER in request.cookies:
        if request.cookies[USER_IDENTIFIER] != "logged-out":
            uid: str = request.cookies.get(USER_IDENTIFIER)
            user_record = User.query.filter_by(uid=uid).first()

            # Getting the stats:
            total_games = GameStats.query.filter_by(uid=uid).count()
            games_finished = GameStats.query.filter_by(uid=uid, game_result=1).order_by(
                GameStats.start_time.desc()).all()

            # Getting the fastest times of completion:
            diff_ft_info = []

            for i in range(NUM_OF_DIFFICULTIES):
                ft_info = get_fastest_time(uid, i + 1)
                if ft_info is not None:
                    diff_ft, diff_ft_date = ft_info[0], ft_info[1]
                else:
                    diff_ft, diff_ft_date = None, ""

                diff_ft_info += [(diff_ft, diff_ft_date)]

            # Getting the count of games of each difficulty:
            diff_count_info = get_games_per_diff(uid)

    else:
        return redirect(url_for('login_blueprint.login_window'))

    if request.method == "POST":
        # Checking which POST request was made by the client (start a new game or log out):
        if request.headers["Content-Type"] == "application/x-www-form-urlencoded":
            difficulty = request.form.get("difficulty")
            diff_id = DIFFICULTY_DICT[difficulty]

            DIFF_RESP.set_cookie(DIFF_CHOSEN, str(diff_id))

            return DIFF_RESP

        elif request.headers["Content-Type"] == "application/json":
            content = request.get_json()

            if "log-out" in content:
                response = make_response(json.dumps({"success": True}), 302)
                response.headers['Content-Type'] = 'application/json'
                response.set_cookie(USER_IDENTIFIER, "logged-out")  # Updating the user cookie to "logged-out"

                return response

    if request.method == "GET":
        # Checking if the GET request is from the client, and not a redirect:
        if request.headers["Accept"] == "application/json":
            completed_games_info = {"entry-id": [], "difficulty": [], "hints-used": [], "time-taken": [],
                                    "date-time": []}

            # Sending the latest (upto) five games to the client (JS):
            for cg in games_finished[:5]:
                cg: GameStats

                diff: str = list(filter(lambda key: DIFFICULTY_DICT[key] == cg.game_type, DIFFICULTY_DICT))[
                    0]  # Returns a list which contains all keys having the value of "game_type"
                completed_games_info["difficulty"] += [diff.capitalize()]

                completed_games_info["entry-id"] += [cg.entry_id]
                completed_games_info["hints-used"] += [cg.hints_used]

                cg_timedelta: datetime.timedelta = cg.end_time - cg.start_time
                time_taken = get_timer_value(cg_timedelta)
                completed_games_info["time-taken"] += [time_taken]

                completed_games_info["date-time"] += [
                    [format_datetime(cg.end_time, type="date"), format_datetime(cg.end_time, type="time")]]

            cg_info_response = make_response(json.dumps(completed_games_info), 200)

            return cg_info_response

    return render_template(
        "home-window.html",
        username=user_record.username, email=user_record.email, join_date=format_datetime(user_record.date_joined),

        total_games=total_games,
        games_completed=len(games_finished),

        s_fastest_time=diff_ft_info[0][0], s_ft_date=diff_ft_info[0][1],
        m_fastest_time=diff_ft_info[1][0], m_ft_date=diff_ft_info[1][1],
        c_fastest_time=diff_ft_info[2][0], c_ft_date=diff_ft_info[2][1],

        simple_cg=diff_count_info[0][0], simple_tg=diff_count_info[0][1],
        medium_cg=diff_count_info[1][0], medium_tg=diff_count_info[1][1],
        complex_cg=diff_count_info[2][0], complex_tg=diff_count_info[2][1],

        simple_min=SIMPLE[0], simple_max=SIMPLE[-1],
        medium_min=MEDIUM[0], medium_max=MEDIUM[-1],
        complex_min=COMPLEX[0], complex_max=COMPLEX[-1]
    )
