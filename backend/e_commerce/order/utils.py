from datetime import datetime, timedelta

import holidays


def format_time(time: int) -> str:
    "Format a time in seconds from seconds to the format hh:mm:ss"
    # construct hour
    if time > 3600:
        hours = time // 3600
        time = time - (hours * 3600)
    else:
        hours = 0

    # construct minutes
    if time > 60:
        minutes = time // 60
        time = time - (minutes * 60)
    else:
        minutes = 0

    hours = hours if hours >= 10 else f"0{hours}"
    minutes = minutes if minutes >= 10 else f"0{minutes}"
    seconds = time if time >= 10 else f"0{time}"

    return f"{hours}:{minutes}:{seconds}"


def add_business_days(date: datetime, business_days: int) -> datetime:
    "Add business days to a `datetime` object by excluding weekends and holidays."
    ir_holidays = holidays.IR()
    added_days = 0
    current_date = date
    THURSDAY, FRIDAY = 2, 3  # weekends 

    while added_days < business_days:
        current_date += timedelta(days=1)
        if (
            current_date.weekday() not in (THURSDAY, FRIDAY)
            and current_date.date() not in ir_holidays
        ):
            added_days += 1

    return current_date
