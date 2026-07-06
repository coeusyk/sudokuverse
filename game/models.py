import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    uid = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    phash = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.DateTime, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().date())

    stats = db.relationship('GameStats', backref='User', lazy=True)


class GameStats(db.Model):
    __tablename__ = "game_stats"

    entry_id = db.Column(db.String(36), primary_key=True)
    uid = db.Column(db.String(36), db.ForeignKey('user.uid'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    hints_used = db.Column(db.Integer, nullable=True)
    game_result = db.Column(db.Integer, nullable=False)  # 0 -> Quit, 1 -> Finish
    game_type = db.Column(db.Integer, nullable=False)  # 1 -> Simple, 2 -> Medium, 3 -> Complex
