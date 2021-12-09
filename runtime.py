def run_time_str(ms: int) -> str:
    """ Converts input milliseconds into formated time string """
    
    hours = ms // 3600000
    ms_after_hours = ms % 3600000
    minutes = ms_after_hours // 60000
    ms_after_minutes = ms_after_hours % 60000
    seconds = ms_after_minutes // 1000
    # ms_left = ms_after_minutes % 1000

    time_str = ""
    if hours != 0:
        time_str += f"{hours:02d}:"

    time_str += f"{minutes:02d}:{seconds:02d}"
    
    return time_str


if __name__ == "__main__":
    ms = 78001000
    print(run_time_str(ms))


# 1 hour = 60 minutes = 3 600 seconds = 3 600 000 milliseconds
# 1 minute = 60 seconds = 60 000 milliseconds
# 1 second = 1 000 milliseconds