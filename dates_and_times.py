"""
This file handles all date and time related methods
"""

from datetime import datetime, time, date, timedelta


def get_today_date() -> str:
    """Returns today's date in YYYY-MM-DD ISO format"""
    return datetime.today().strftime("%Y-%m-%d")


def get_tomorrow_date() -> str:
    """Returns tomorrow's date in YYYYMMDD format"""
    return (datetime.today() + timedelta(days=1)).date().isoformat()


def get_datetime(given_date: str, given_time: str) -> datetime:
    """
    Get the proper datetime given a date and time

    Date will be in YYYY-MM-DD format
    Time will be in HH:MM format
    """
    try:
        if given_date.lower() == "tomorrow":
            new_date = date.fromisoformat(get_tomorrow_date())
        else:
            new_date = date.fromisoformat(given_date)

    except ValueError as exc:
        raise ValueError(f"Unable to parse given date: {given_date}. "
                         f"It must be in YYYY-MM-DD format") from exc
    try:
        cleaned_time = cleanup_time(given_time + ":00")
        new_time = time.fromisoformat(cleaned_time)
    except ValueError as exc:
        raise ValueError(f"Unable to parse given time: {given_time}. "
                         f"It must be in HH:MM format") from exc

    return datetime.combine(date=new_date, time=new_time)


def get_pretty_date(given_datetime: datetime) -> str:
    """
    Given a datetime, return a human-readable time

    A: weekday as locale's full name
    d: day of the month
    B: month as locale's full name
    Y: year with century as decimal
    I: hour (12-hour clock) as a zero-padded decimal number
    M: minute as a zero-padded decimal number
    p: locale’s equivalent of either AM or PM
    """
    return given_datetime.strftime("%A, %d. %B %Y %I:%M%p")


def get_pretty_time(iso_time: str) -> str:
    """Given an ISO format HH:MM:SS, return the time in 12hr HH:MM AM/PM format"""
    return time.fromisoformat(cleanup_time(iso_time)).strftime("%I:%M %p")


def get_iso_time(given_datetime: datetime) -> str:
    """Get the ISO HH:MM:SS time given a datetime"""
    return given_datetime.time().isoformat()


def get_iso_date(given_datetime: datetime) -> str:
    """Get the ISO YYYY-MM-DD date given a datetime"""
    return given_datetime.date().isoformat()


def get_njt_date(given_datetime: datetime) -> str:
    """Get the date in a YYYYMMDD format"""
    return given_datetime.strftime("%Y%m%d")


def cleanup_time(given_time: str) -> str:
    """
    This function exists to clean the hours of an ISO HH:MM:SS time
    NJ Transit has times that spill over into the next day
    EX: 1:30 AM the next day as 25:30:00
    """
    if len(given_time) != 8:
        raise ValueError
    tokens = given_time.split(':')
    tokens = [int(token) for token in tokens]
    tokens[0] %= 24

    return time(*tokens).isoformat()
