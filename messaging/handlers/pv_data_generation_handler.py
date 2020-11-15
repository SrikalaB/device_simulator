from profiles.constants import *
from profiles.profile import PvProfile
import datetime
import csv

class PvDataGenerationHandler(object):

    def __init__(self, message):
        self.payload_type = message.get("payload_type")
        self.meter_power_value = message.get("value")
        self.meter_power_unit = message.get("unit")
        self.timestamp = datetime.datetime.strptime(message.get("timestamp"), "%Y-%m-%d %H:%M:%S")

    @property
    def meter_power_value(self):
        return self._meter_power_value

    @meter_power_value.setter
    def meter_power_value(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Meter reading should be a number")
        self._meter_power_value = value

    @property
    def meter_power_unit(self):
        return self._meter_power_unit

    @meter_power_unit.setter
    def meter_power_unit(self, value):
        if value not in ALLOWED_UNITS:
            raise ValueError("Meter value's unit incomprehensible")
        self._meter_power_unit = value

    def call(self):
        pv_value, _unit = PvProfile().get_value_at_time(self.timestamp, self.meter_power_unit)
        # Negating value to indicate that Pv value indicates power production and not consumption
        pv_value = -pv_value
        self.write_values_to_csv(self.timestamp, pv_value, self.meter_power_value, self.meter_power_unit)

    def write_values_to_csv(self, timestamp, meter_value, pv_value, unit):
        file_name = "{}_meter_with_pv.csv".format(timestamp.strftime("%Y-%m-%d"))
        fields = ["timestamp", "Meter value", "PV value", "Net load", "unit"]
        with open(file_name, 'a') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(fields)
            writer.writerow([timestamp, meter_value, pv_value, meter_value+pv_value, unit])
        print("Wrote to csv pv- {} meter- {} unit-{}".format(pv_value, meter_value, unit))
