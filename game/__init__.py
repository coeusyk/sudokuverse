from flask import Flask, render_template, redirect, url_for

import os
import toml

from game.core.auth import is_logged_in
from game.core.constants import COOKIE_EXPIRATION_TIME


def create_app():
    """
    Creates a Flask app and configures all basic requirements to run the web server
    """

    profile = os.getenv('APP_PROFILE')
    if profile is None:
        profile = "dev"

    from game.config import Config
    config = Config(flask_env=profile)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.toml", load=toml.load)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_uri()
    app.config['SECRET_KEY'] = config.get_secret_key()
    app.config['PERMANENT_SESSION_LIFETIME'] = COOKIE_EXPIRATION_TIME
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = profile == "prod"
    app.app_context().push()

    from game.models import db
    db.init_app(app)
    db.create_all()

    # Registering all blueprints:
    from game.ui.gameplay import gameplay
    app.register_blueprint(gameplay.gameplay_blueprint)

    from game.ui.play import play
    app.register_blueprint(play.play_blueprint)

    from game.ui.signup import signup
    app.register_blueprint(signup.signup_blueprint)

    from game.ui.home import home
    app.register_blueprint(home.home_blueprint)

    from game.ui.login import login
    app.register_blueprint(login.login_blueprint)

    from game.ui.about import about
    app.register_blueprint(about.about_blueprint)

    from game.ui.learn import learn
    app.register_blueprint(learn.learn_blueprint)

    @app.route("/")
    def main_window():
        if is_logged_in():
            return redirect(url_for("home_blueprint.home_window"), code=302)

        return render_template("main-window.html")

    return app
