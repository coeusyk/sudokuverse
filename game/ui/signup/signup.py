import json
import uuid

from flask import Blueprint, render_template, request, make_response, redirect, url_for
from werkzeug.security import generate_password_hash

from game.core.auth import is_logged_in, login_user
from game.core.signup_work import check_username_validity, check_email_validity, check_phash_validity, \
    validate_and_format_date
from game.models import db, User

signup_blueprint = Blueprint("signup_blueprint", __name__, template_folder="templates", static_folder="static",
                             static_url_path="/ui/signup")


@signup_blueprint.route("/signup", methods=["GET", "POST"])
def signup_window():
    if is_logged_in():
        return redirect(url_for('home_blueprint.home_window'), code=302)

    if request.method == "POST":
        username = request.form.get("username")
        dob = request.form.get("dob")
        email = request.form.get("email")
        phash = request.form.get("phash")

        uname_validity = check_username_validity(username)
        dob_validity = validate_and_format_date(dob)
        email_validity = check_email_validity(email)
        phash_validity = check_phash_validity(phash)

        if (uname_validity and email_validity and phash_validity) and (
                dob_validity or not isinstance(dob_validity, str)):
            phash = generate_password_hash(phash)

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

            login_user(uid)

            response = make_response(json.dumps({"success": True}), 302)
            response.headers['Content-Type'] = 'application/json'

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
