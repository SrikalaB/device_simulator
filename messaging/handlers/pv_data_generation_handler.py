from profiles.constants import *
from profiles.profile import PvProfile
import datetime
import csv
from utils import calculate_net_load


class PvDataGenerationHandler(object):

    def __init__(self, message):
        self.message = message
        try:
            self.payload_type = self.message.get("payload_type")
            self.meter_power_value = self.message.get("value")
            self.meter_power_unit = self.message.get("unit")
            self.timestamp = datetime.datetime.strptime(self.message.get("timestamp"), "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print("Unable to execute handler due to incorrect message format - {}".format(str(e)))
            raise e

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

    def __call__(self):
        """
        Gets value from PV profile for the timestamp of meter value. Calculates net load and writes all values to csv
        :return:
        """
        pv_value, _unit = PvProfile().get_value_at_time(self.timestamp, self.meter_power_unit)

        fields = ["timestamp", "Meter value", "PV value", "Net load", "unit"]
        net_load = calculate_net_load(self.meter_power_value, pv_value)
        self.write_values_to_csv_row(self.output_filename(), [self.timestamp, self.meter_power_value, pv_value,
                                     net_load, self.meter_power_unit], fields)

    @staticmethod
    def write_values_to_csv_row(filename, values_row, header=None):
        """
        Writes a row content to a csv.
        :param filename: str Full file path of csv
        :param header: List [Optional] Header row of csv
        :param values_row: List Values to be written in row
        :return:
        """
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                if header is not None:
                    writer.writerow(header)
            writer.writerow(values_row)
            print("Completed writing row to file {}".format(values_row))

    def output_filename(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                            "output_files", "{}_meter_with_pv.csv".format(self.timestamp.strftime("%Y-%m-%d")))
