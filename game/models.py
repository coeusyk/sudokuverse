from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# class User(db.Model):
#     __tablename__ = "user"

#     uid = db.Column(db.String(36), primary_key=True)
#     username = db.Column(db.String(25), nullable=False, unique=True)
#     email = db.Column(db.String(256), nullable=False, unique=True)
#     phash = db.Column(db.String(32), nullable=False)


# class UserProfile(db.Model):
#     __tablename__ = "user_profile"

#     uid = db.Column(db.String(36), db.ForeignKey("user.uid"))
#     dob = db.Column(db.DateTime, nullable=False)


# class GameStats(db.Model):
#     __tablename__ = "game_stats"

#     uid = db.Column(db.String(36), db.ForeignKey("user.uid"))
#     wins = db.Column(db.Integer, nullable=False)
#     losses = db.Column(db.Integer, nullable=False)
#     game_type = db.Column(db.Integer, nullable=False)


# class TimeStats(db.Model):
#     __tablename__ = "time_stats"

#     uid = db.Column(db.String(36), db.ForeignKey("user.uid"))
