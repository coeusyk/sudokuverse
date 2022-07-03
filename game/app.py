from flask import Flask, render_template

from ui.play import play_blueprint


app = Flask(__name__)
app.register_blueprint(play_blueprint)


@app.route("/")
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=False)
