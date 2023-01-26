import re
import datetime

from game.models import *


def check_username_validity(username: str):
    """
    Checks if the username has already been used or not and if the username is greater than 4 letters
    - Returns:- True if valid, else the error key

    `username`: The username chosen by the user
    """

    regular_expression = "[a-zA-Z0-9]{5,25}"

    if len(username) == 0:
        return "not-entered"
    
    elif not (5 <= len(username) <= 25):
        return "invalid-length"
    
    elif not re.fullmatch(regular_expression, username):
        return "invalid-format"
    
    else:
        username_check = User.query.filter(User.username.ilike(username)).one_or_none()

        if username_check != None:
            return "taken"
    
    return True


def check_email_validity(email: str):
    """
    Checks if the email given has already been used or not and if it follows the syntax
    - Returns:- True if valid, else the error key

    `email`: The email given by the user
    """

    regular_expression = r"[a-zA-Z0-9!#$%&*+./=?^-_`{|}~]+@[a-zA-Z0-9.-]+\." \
                         r"[A-Z|a-z]{2,}$"

    if len(email) == 0:
        return "not-entered"
    
    elif len(email) > 255:
        return "invalid-length"
    
    elif not re.fullmatch(regular_expression, email):
        return "invalid-format"

    else:
        # Checking if a record having the entered email exists:
        email_check = User.query.filter(User.email.ilike(email)).one_or_none()

        if email_check != None:
            return "taken"

    return True


def check_phash_validity(phash: str):
    """
    Checks if the phash entered is valid
    - Returns:- True if valid, else the error key

    `phash`: The phash entered by the user
    """

    if len(phash) == 0:
        return "not-entered"
    
    elif len(phash) < 6:
        return "invalid-length"

    special_chars = "!@#$%^&*)(}{][:;?/><|\"\'.,+=_-~`"

    invalid_char, invalid_char_count = None, 0

    for i in phash:
        if not (
            (64 < ord(i) < 91) and not (96 < ord(i) < 123) and 
            (i not in special_chars) and not (47 < ord(i) < 58)
        ):
            invalid_char_count += 1
            if invalid_char_count == 2:
                return "invalid-format-2"
            else:
                invalid_char = i
    else:
        if invalid_char_count == 1:
            return ["invalid-format-1", invalid_char]
    
    return True


def validate_N_format_date(date: str):
    """
    Checks if the entered date is valid
    - Returns:- The formatted datetime value if valid, else the error key

    `date`: The date entered by the user
    """

    if date == "":
        return True
    
    else:
        parts = date.split("-")
        year = [int(i) for i in parts][0]

        present_time = datetime.datetime.now().date()

        if year <= present_time.year:
            try:
                entered_datetime = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return "invalid-format"

            entered_date = entered_datetime.date()

            time_difference = present_time - entered_date
            approx_years = time_difference.days / 365

            if (5 <= approx_years <= 130):
                return entered_date
            elif approx_years < 5:
                return "underage"
            else:
                return "overage"
        
        else:
            return "invalid-age"
