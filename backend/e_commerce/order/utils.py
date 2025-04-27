def format_time(time: int) -> str:
    "Format a time from total seconds to format of hh:mm:ss"
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
