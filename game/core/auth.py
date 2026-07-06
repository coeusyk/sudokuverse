from flask import session


def is_logged_in() -> bool:
    return "uid" in session


def current_uid() -> str | None:
    return session.get("uid")


def login_user(uid: str) -> None:
    session.permanent = True
    session["uid"] = uid


def logout_user() -> None:
    session.pop("uid", None)
