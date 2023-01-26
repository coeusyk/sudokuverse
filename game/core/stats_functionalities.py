import datetime

from game.models import GameStats
from game.core.constants import NUM_OF_DIFFICULTIES


def format_datetime(date_time: datetime.datetime, type="date"):
    """
    Formats datetime object to "dd Month (first three characters) yyyy" or "HH:MM AM/PM"
    - Returns:- The formatted datetime value

    `date_time`:- The datetime object entered
    `type`:- The format of the datetime object to be converted to
    """

    if type == "date":
        date = date_time.strftime("%d %b %Y")
        return date

    elif type == "time":
        time = date_time.strftime("%I:%M%p")
        return time
    
    else:
        format_type_error = "invalid format type: expected \'date\' or \'time\'"
        raise ValueError(format_type_error)


def get_games_per_diff(uid: str):
    """
    Gets the count of completed games and total games in each difficulty played by the user
    - Returns:- The completed and total games (format:- `Completed Games / Total Games`)

    `uid`:- The unique identifier of the user 
    """

    diff_games_info = []
    
    for i in range(NUM_OF_DIFFICULTIES):
        completed_games = GameStats.query.filter_by(uid=uid, game_type=(i + 1), game_result=1).count()
        total_games = GameStats.query.filter_by(uid=uid, game_type=(i + 1)).count()

        diff_games_info += [(completed_games, total_games)]
    
    return diff_games_info


def seconds_to_proper_time(time: int):
    """
    Converts the entered seconds into hours, minutes and seconds
    - Returns:- The converted proper time (hours, minutes, seconds)

    `time`:- Number of seconds
    """

    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time - ((hours * 3600) + (minutes * 60))

    return hours, minutes, seconds


def get_timer_value(game_timedelta: datetime.timedelta):
    """
    Converts the entered game timedelta to MM:SS (or HH:MM:SS)
    - Returns:- The timer value

    `game_timedelta`:- The timedelta of the game
    """

    hours, minutes, seconds = seconds_to_proper_time(int(game_timedelta.total_seconds()))

    if hours == 0:
        if seconds < 10:
            timer_value = f"{minutes}:0{seconds}"
        else:
            timer_value = f"{minutes}:{seconds}"
    else:
        timer_value = f"{hours}:{datetime.time(minute=minutes, second=seconds).strftime('%M:%S')}"

    return timer_value


def get_fastest_time(uid: str, diff_id: int):
    """
    Gets the fastest time of completion of the user and the date in the specified difficulty
    - Returns:- The fastest time and date (on which it was achieved), None otherwise

    `uid`:- The unique identifier of the user
    `diff_id`:- The difficulty id
    """

    records: list[GameStats] = GameStats.query.filter_by(uid=uid, game_type=diff_id, game_result=1).all()

    if len(records) == 0:
        return None

    else:
        ft_record = None  # ft -> fastest time
        fastest_timedelta = datetime.timedelta(hours=(365 * 24))

        for record in records:
            time_delta: datetime.timedelta = record.end_time - record.start_time

            if time_delta < fastest_timedelta:
                fastest_timedelta, ft_record = time_delta, record


    if ft_record == None:
        return None
    
    else:
        timer_value = get_timer_value(fastest_timedelta)

        return f"{timer_value} ", f"({format_datetime(record.end_time, type='date')})"


def convert_timer_value(time: int | None):  # For gameplay.py
    """
    Converts the obtained timer value (when not `None`) to timedelta value
    - Returns:- The converted timedelta value

    `time`:- The timer value obtained (in seconds) from the client
    """

    if time == None:
        return None

    hours, minutes, seconds = seconds_to_proper_time(time)
    timer_timedelta = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours)
    
    return timer_timedelta
