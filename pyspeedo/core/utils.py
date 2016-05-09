import time


def current_time_millisec():
    return int(round(time.time() * 10**3))
