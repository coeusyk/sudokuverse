from flask import Flask, render_template

from play_window.play import play_window_blueprint


app = Flask(__name__)
app.register_blueprint(play_window_blueprint, url_prefix='/play_window')


@app.route("/")
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=False)
