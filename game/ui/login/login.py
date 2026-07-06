import json

from flask import Blueprint, render_template, request, redirect, url_for, make_response

from game.core.auth import is_logged_in, login_user
from game.core.login_work import validate_login_credentials


login_blueprint = Blueprint("login_blueprint", __name__, template_folder="templates", static_folder="static",
                            static_url_path="/ui/login")


@login_blueprint.route("/login", methods=["GET", "POST"])
def login_window():
    if is_logged_in():
        return redirect(url_for('home_blueprint.home_window'), code=302)

    if request.method == "POST":
        email = request.form.get("email")
        phash = request.form.get("phash")

        login_validation = validate_login_credentials(email, phash)

        if login_validation:
            _, user_record = login_validation
            login_user(user_record.uid)

            response = make_response(json.dumps({"success": True}), 302)

            return response

        else:
            response = make_response(json.dumps({"success": False}), 200)

            return response

    return render_template("login-window.html")
