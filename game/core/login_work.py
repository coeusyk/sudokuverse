import hashlib

from game.models import *


def validate_login_credentials(email: str, phash: str):
    """
    Validates the login credentials of a user.

    Args:
        email (str): The email address of the user.
        phash (str): The plaintext password hash provided by the user.

    Returns:
        tuple: A tuple (True, user_record) if the credentials are valid,
        where `user_record` is the user's database record.

        bool: False if the credentials are invalid.
    """

    if not (0 < len(email) < 256):
        return False

    else:
        # Checking if a user with the entered email exists:
        user_record = User.query.filter(User.email.ilike(email)).one_or_none()

        if user_record is not None:
            if len(phash) < 6:
                return False

            phash = hashlib.md5(phash.encode('utf-8')).hexdigest()

            if user_record.phash == phash:
                return True, user_record

    return False
