"""
This file handles all date and time related methods
"""

from datetime import datetime, time, timedelta


def get_today_date() -> str:
    """Returns today's date in YYYYMMDD format"""
    return datetime.today().strftime("%Y%m%d")


def get_tomorrow_date() -> str:
    """Returns tomorrow's date in YYYYMMDD format"""
    return (datetime.today() + timedelta(days=1)).strftime("%Y%m%d")


def get_datetime(given_date: str):
    """
    Return a datetime object of the given_date
    Has checks to see if it is the current day or not
    """
    if len(given_date) != 8:
        raise ValueError(f"Unable to parse given date: {given_date}")

    try:
        if given_date == get_today_date():
            return datetime.today()
        return datetime(year=int(given_date[0:4]),
                        month=int(given_date[4:6]),
                        day=int(given_date[6:8]))
    except ValueError as exc:
        raise ValueError(f"Unable to parse given date: {given_date}") from exc


def get_pretty_date(given_date: str) -> str:
    """Returns the datetime in a human-readable format"""
    return get_datetime(given_date).strftime("%A, %d. %B %Y %I:%M %p")


def get_time(given_date: str) -> str:
    """Returns the time given a date in a HH:MM:SS format"""
    return get_datetime(given_date).strftime("%H:%M:%S")


def get_pretty_time(given_time: str) -> str:
    """Returns the time in a human-readable format given a HH:MM:SS format"""
    tokens = given_time.split(':')
    tokens = [int(token) for token in tokens]
    tokens[0] %= 24

    return time(*tokens).strftime("%I:%M %p")
