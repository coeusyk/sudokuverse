import hashlib
import json
import uuid

from flask import Blueprint, render_template, request, make_response, redirect, url_for

from game.core.signup_work import check_username_validity, check_email_validity, check_phash_validity, \
    validate_N_format_date
from game.models import db, User
from game.core.constants import USER_IDENTIFIER, COOKIE_EXPIRATION_TIME

signup_blueprint = Blueprint("signup_blueprint", __name__, template_folder="templates", static_folder="static",
                             static_url_path="/ui/signup")


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

        if (uname_validity and email_validity and phash_validity) and (
                dob_validity or not isinstance(dob_validity, str)):
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

            response = make_response(json.dumps({"success": True}), 302)
            response.headers['Content-Type'] = 'application/json'

            user_cookie_expiration = user_record.date_joined + COOKIE_EXPIRATION_TIME
            response.set_cookie(USER_IDENTIFIER, uid, expires=user_cookie_expiration)

            return response

        else:
            errors = {"success": False}

            # Adding the errors:
            if not uname_validity:
                errors["username"] = uname_validity
            if not email_validity:
                errors["email"] = email_validity
            if not phash_validity:
                errors["phash"] = phash_validity
            if isinstance(dob_validity, str):
                errors["dob"] = dob_validity

            # Sending the response containing the errors made to JavaScript:
            response = make_response(json.dumps(errors), 200)

            return response

    return render_template("signup-window.html")
