import datetime


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
    if pv_value <= 0:
        pass
    else:
        # Negating value to indicate that Pv value indicates power production and not consumption
        pv_value = -pv_value
    return round(float(meter_value + pv_value), 2)
