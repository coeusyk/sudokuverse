from game.models import *


def check_username_validity(username: str):
    """
    Checks if the username has already been used or not and if the username is greater than 4 letters
    - Returns:- True if valid, else the error key

    `username`: The username chosen by the user
    """

    if username is None:
        return "not-entered"
    
    elif not (5 <= len(username) <= 25):
        return "invalid-length"
    
    else:
        username_check = db.session.execute(db.select(User).filter_by(username=username)).one_or_none()

        if username_check != None:
            return "taken"
    
    return True


def check_email_validity(email: str):
    """
    Checks if the email given has already been used or not and if it follows the syntax
    - Returns:- True if valid, else the error key

    `email`: The email given by the user
    """

    import re

    regular_expression = r"[a-zA-Z0-9!#$%&*+./=?^-_`{|}~]+@[a-zA-Z0-9.-]+\.[A-Z|a-z]{2,}$"

    if email is None:
        return "not-entered"
    
    elif len(email) > 256:
        return "invalid-length"
    
    elif not re.fullmatch(regular_expression, email):
        return "invalid-format"

    else:
        # Checking if a record having the entered email exists:
        email_check = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()

        if email_check != None:
            return "taken"

    return True


def check_phash_validity(phash: str):
    """
    Checks if the phash entered is valid
    - Returns:- Phash strength if valid, else the error key

    `phash`: The phash entered by the user
    """

    if phash is None:
        return "not-entered"
    
    elif len(phash) < 6:
        return "invalid-length"

    special_chars = "!@#$%^&*)(}{][:;?/><|\"\'.,+=_-~`"

    invalid_char, invalid_char_count = None, 0

    for i in phash:
        if not (64 < ord(i) < 91) and not (96 < ord(i) < 123) and (i not in special_chars) and (48 < ord(i) < 57):
            invalid_char_count += 1
            if invalid_char_count == 2:
                return "invalid-format-2"
            else:
                invalid_char = i
    else:
        if invalid_char_count == 1:
            return ["invalid-format-1", invalid_char]
    
    return True
