import unittest
import mock
from messaging.handlers.pv_data_generation_handler import PvDataGenerationHandler
import copy


class TestPvDataGenerationHandler(unittest.TestCase):
    valid_message = {"timestamp": "2020-11-17 20:51:00",
                     "value": 6573.22,
                     "device": "meter123",
                     "unit": "W",
                     "payload_type": "meter_data"}

    @mock.patch("messaging.handlers.pv_data_generation_handler.calculate_net_load")
    def test_call(self, calculate_net_load_mock):
        with mock.patch("messaging.handlers.pv_data_generation_handler.PvProfile") as profile_mock:
            csv_row_mock = mock.Mock()
            PvDataGenerationHandler.write_values_to_csv_row = csv_row_mock
            profile_mock.return_value.get_value_at_time.return_value = (1234, "W")
            profile_mock.TYPE.return_value = "PvProfile"

            PvDataGenerationHandler(TestPvDataGenerationHandler.valid_message)()
            calculate_net_load_mock.assert_called_once_with(6573.22, 1234)
            self.assertTrue(csv_row_mock.called)

    def test_validation(self):
        message = copy.copy(TestPvDataGenerationHandler.valid_message)
        message["value"] = "wrong_value"
        try:
            PvDataGenerationHandler(message)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        message['value'] = 1234
        message['unit'] = "nonsensical"
        try:
            PvDataGenerationHandler(message)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)


