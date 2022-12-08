import uuid

from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    uid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    phash = db.Column(db.String(32), nullable=False)
    dob = db.Column(db.DateTime, nullable=True)

    stats = db.relationship('GameStats', backref='User', lazy=True)


class GameStats(db.Model):
    __tablename__ = "game_stats"

    entry_id = db.Column(db.String(36), primary_key=True)
    uid = db.Column(db.String(36), db.ForeignKey('user.uid'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    game_result = db.Column(db.Integer, nullable=False)  # 0 -> Quit, 1 -> Win, -1 -> Loss
    game_type = db.Column(db.Integer, nullable=False)
