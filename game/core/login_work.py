"""
This file is for validating the login credentials entered by the user
"""


import hashlib

from game.models import *


def validate_login_credentials(email: str, phash: str):
    if not (0 < len(email) < 256):
        return False
    
    else:
        # Checking if a user with the entered email exists:
        user_record = User.query.filter(User.email.ilike(email)).one_or_none()

        if user_record != None:
            if len(phash) < 6:
                return False

            phash = hashlib.md5(phash.encode('utf-8')).hexdigest()

            if user_record.phash == phash:
                return True, user_record
    
    return False
