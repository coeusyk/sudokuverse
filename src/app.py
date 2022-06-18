from flask import Flask, render_template


app = Flask(__name__)

"""
@app.get("/")
def main_window():
    return render_template("main_window/title-bar.html")
"""

if __name__ == "__main__":
    app.run()
