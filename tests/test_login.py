"""
Self-check for the login fix: validate_login_credentials previously returned
an inverted result (a truthy tuple was treated as failure), and passwords were
hashed with unsalted MD5. Run: python tests/test_login.py
"""
from flask import Flask
from werkzeug.security import generate_password_hash

from game.models import db, User
from game.core.login_work import validate_login_credentials


def run():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.app_context().push()
    db.init_app(app)
    db.create_all()

    user = User(uid="test-uid", username="tester1", email="test@example.com",
                phash=generate_password_hash("correct-password"))
    db.session.add(user)
    db.session.commit()

    ok = validate_login_credentials("test@example.com", "correct-password")
    assert ok is not False and ok[0] is True and ok[1].uid == "test-uid", f"expected success tuple, got {ok}"

    bad = validate_login_credentials("test@example.com", "wrong-password")
    assert bad is False, f"expected False for wrong password, got {bad}"

    missing = validate_login_credentials("nobody@example.com", "whatever1")
    assert missing is False, f"expected False for unknown email, got {missing}"

    print("OK: login validation + password hashing self-check passed")


if __name__ == "__main__":
    run()
