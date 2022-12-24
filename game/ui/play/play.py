import json
import hashlib

from flask import Blueprint, render_template, request, redirect, url_for, session

from game.core.constants import CELL_ATTRIBUTES
from game.core.signup_work import check_username_validity, check_email_validity, check_phash_validity
from game.models import db, User


play_blueprint = Blueprint("play_blueprint", __name__, template_folder="templates", static_folder="static", static_url_path="/ui/play")


@play_blueprint.route("/play/guest", methods=['GET', 'POST'])
def play_window_guest():
    uname_validity, email_validity, phash_validity = None, None, None

    if request.method == "POST":
        # Checking if the request from JS is for adding a user:
        if "add-user" in request.form:
            username = request.form.get("username")
            dob = request.form.get("dob")
            email = request.form.get("email")
            phash = request.form.get("phash")

            uname_validity = check_username_validity(username)
            email_validity = check_email_validity(email)
            phash_validity = check_phash_validity(phash)

            if (uname_validity == True) and (email_validity == True) and (phash_validity == True):
                phash = hashlib.md5(phash)

                user_record = User(
                    username=username, 
                    email=email, 
                    phash=phash, 
                    dob=dob
                )

                db.session.add(user_record)

                return redirect(f"/play/{username}")  # Redirecting to the user window
        
        # Checking if the request from JS is for redirecting the user to the gameplay window:
        elif "redirect" in request.form:
            difficulty = request.form.get("difficulty")

            session['game-info'] = json.dumps({"difficulty": difficulty})

            return redirect(url_for('gameplay_blueprint.gameplay_window'))  # Redirecting to the game window

    return render_template(
        "play-window_guest.html", 
        cell_attributes=CELL_ATTRIBUTES, 
        uname_val=uname_validity, 
        email_val=email_validity, 
        phash_val=phash_validity
    )


@play_blueprint.route("/play/<username>")
def play_window_user(username: str):
    user = User.query.filter_by(username=username).first_or_404()  # Getting the logged-in user

    return render_template(
        "play-window_user.html", 
        user=user
    )
