import os
METER_PROFILE_24H_FILEPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profile_csvs', 'load_24h.csv')
PV_PROFILE_24H_FILEPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profile_csvs', 'solar_24h.csv')

# Units

WATTS = "W"
KILO_WATTS = "kW"

ALLOWED_UNITS = [WATTS, KILO_WATTS]