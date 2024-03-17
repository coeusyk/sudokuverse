import json

from flask import Blueprint, render_template, request, redirect, url_for, make_response

from game.core.login_work import validate_login_credentials
from game.core.constants import USER_IDENTIFIER, COOKIE_EXPIRATION_TIME


login_blueprint = Blueprint("login_blueprint", __name__, template_folder="templates", static_folder="static",
                            static_url_path="/ui/login")


@login_blueprint.route("/login", methods=["GET", "POST"])
def login_window():
    if USER_IDENTIFIER in request.cookies:
        if request.cookies[USER_IDENTIFIER] != "logged-out":
            return redirect(url_for('home_blueprint.home_window'), code=302)
    
    if request.method == "POST":
        email = request.form.get("email")
        phash = request.form.get("phash")

        login_validation = validate_login_credentials(email, phash)
        
        if login_validation is not False:
            user_record = login_validation[1]

            response = make_response(json.dumps({"success": True}), 302)
            response.headers['Content-Type'] = 'application/json'

            user_cookie_expiration = user_record.date_joined + COOKIE_EXPIRATION_TIME
            response.set_cookie(USER_IDENTIFIER, user_record.uid, expires=user_cookie_expiration)

            return response
        
        else:
            response = make_response(json.dumps({"success": False}), 200)

            return response

    return render_template("login-window.html")
