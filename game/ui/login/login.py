import json

from flask import Blueprint, render_template, request, redirect, url_for, Response

from game.core.login_work import validate_login_credentials
from game.core.constants import USER_IDENTIFIER, COOKIE_EXPIRATION_TIME, SUCCESS_RESP


login_blueprint = Blueprint("login_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/login")


@login_blueprint.route("/login", methods=["GET", "POST"])
def login_window():
    if USER_IDENTIFIER in request.cookies:
        if request.cookies[USER_IDENTIFIER] != "logged-out":
            return redirect(url_for('home_blueprint.home_window'), code=302)
    
    if request.method == "POST":
        email = request.form.get("email")
        phash = request.form.get("phash")

        login_validation = validate_login_credentials(email, phash)
        
        if type(login_validation) == tuple:
            user_record = login_validation[1]

            user_cookie_expiration = user_record.date_joined + COOKIE_EXPIRATION_TIME
            SUCCESS_RESP.set_cookie(USER_IDENTIFIER, user_record.uid, expires=user_cookie_expiration)

            return SUCCESS_RESP
        
        else:
            response = Response(response=json.dumps({"success": False}), status=200)

            return response

    return render_template("login-window.html")
