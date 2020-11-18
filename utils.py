import datetime
import sys
import time


def round_time(dt=None, date_delta=datetime.timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    round_to = date_delta.total_seconds()

    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+round_to/2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)


def calculate_net_load(meter_value, pv_value):
    """
    Subtracts PV value from meter value to calculate net load of consumption. Negates PV value if it is not already negative
    :param meter_value: float.
    :param pv_value: float
    :return: net_load: float.
    """
    if pv_value <= 0:
        pass
    else:
        # Negating value to indicate that Pv value indicates power production and not consumption
        pv_value = -pv_value
    return round(float(meter_value + pv_value), 2)


def on_error_retry(func):
    """
    :param func: The function that needs to be executed
    :return: Function's output If the method execution is successful,
            else sleep and retry again in some time.
    """

    def wrapper(*args, **kwargs):
        max_retries = 10
        timeout = 5
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                time.sleep(timeout)
                continue
        else:
            print("Exhausted all retries. Shutting down.. due to connection error")
            sys.exit(1)
    return wrapper
