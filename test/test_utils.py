import unittest
import datetime
from utils import *


class TestUtils(unittest.TestCase):

    def test_round_time(self):
        # Turn the clock back
        timestamp = datetime.datetime(2020, 10, 12, 10, 11, 11)
        rounded_timestamp = round_time(timestamp, datetime.timedelta(minutes=30))
        self.assertEqual(rounded_timestamp, datetime.datetime(2020, 10, 12, 10, 0))

        # Turn the clock forward
        timestamp = datetime.datetime(2020, 10, 12, 10, 11, 11)
        rounded_timestamp = round_time(timestamp, datetime.timedelta(minutes=15))
        self.assertEqual(rounded_timestamp, datetime.datetime(2020, 10, 12, 10, 15))

    def test_calculate_net_load(self):
        # Convert PV value to negative
        pv_value = 3000
        meter_value = 5000
        net_load = calculate_net_load(meter_value, pv_value)
        self.assertEqual(net_load, 2000)

        # Use PV value as is
        pv_value = -3000
        meter_value = 5000
        net_load = calculate_net_load(meter_value, pv_value)
        self.assertEqual(net_load, 2000)

