from flask import Flask, render_template, request, redirect, url_for

import os
import toml

from game.core.constants import USER_IDENTIFIER


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
        if USER_IDENTIFIER in request.cookies:
            if request.cookies[USER_IDENTIFIER] != "logged-out":
                return redirect(url_for("home_blueprint.home_window"), code=302)

        return render_template("main-window.html")

    return app
