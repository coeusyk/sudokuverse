import uuid
import toml

from flask import Flask, render_template


# DATABASE_URI = "mysql+pymysql://root:example@127.0.0.1:3306/sudoku_verse_db_dev"
def create_app():
    from game.config import Config
    config = Config()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.toml", load=toml.load)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_uri()
    app.app_context().push()

    app.config['SECRET_KEY'] = uuid.uuid4().hex  # Setting a secret key

    from game.models import db
    db.init_app(app)
    db.create_all()

    from game.ui.play import play
    app.register_blueprint(play.play_blueprint)

    from game.ui.gameplay import gameplay
    app.register_blueprint(gameplay.gameplay_blueprint)

    @app.route("/")
    def base():
        return render_template("base.html")

    return app
