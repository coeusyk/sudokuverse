import hashlib
import json
import uuid

from flask import Blueprint, render_template, request, Response, redirect, url_for

from game.core.signup_work import check_username_validity, check_email_validity, check_phash_validity, validate_N_format_date
from game.models import db, User
from game.core.constants import USER_IDENTIFIER, COOKIE_EXPIRATION_TIME, SUCCESS_RESP


signup_blueprint = Blueprint("signup_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/signup")


@signup_blueprint.route("/signup", methods=["GET", "POST"])
def signup_window():
    if USER_IDENTIFIER in request.cookies:
        if request.cookies[USER_IDENTIFIER] != "logged-out":
            return redirect(url_for('home_blueprint.home_window'), code=302)

    uname_validity, email_validity, phash_validity = None, None, None

    if request.method == "POST":
        username = request.form.get("username")
        dob = request.form.get("dob")
        email = request.form.get("email")
        phash = request.form.get("phash")

        uname_validity = check_username_validity(username)
        dob_validity = validate_N_format_date(dob)
        email_validity = check_email_validity(email)
        phash_validity = check_phash_validity(phash)

        if (uname_validity == True) and (email_validity == True) and (phash_validity == True) and ((dob_validity == True) or (type(dob_validity) != str)):
            phash = hashlib.md5(phash.encode('utf-8')).hexdigest()

            # Checking if the date was entered or not:
            if len(dob) == 0:
                dob = None
            else:
                dob = dob_validity

            uid = str(uuid.uuid1())

            user_record = User(
                uid=uid,
                username=username,
                email=email, 
                phash=phash, 
                dob=dob
            )

            db.session.add(user_record)
            db.session.commit()

            user_cookie_expiration = user_record.date_joined + COOKIE_EXPIRATION_TIME
            SUCCESS_RESP.set_cookie(USER_IDENTIFIER, uid, expires=user_cookie_expiration)

            return SUCCESS_RESP

        else:
            errors = {"success": False}

            # Adding the errors:
            if uname_validity != True:
                errors["username"] = uname_validity 
            if email_validity != True:
                errors["email"] = email_validity
            if phash_validity != True:
                errors["phash"] = phash_validity
            if type(dob_validity) == str:
                errors["dob"] = dob_validity

            # Sending the response containing the errors made to JavaScript:
            response = Response(response=json.dumps(errors), status=200)

            return response
    
    return render_template("signup-window.html")
