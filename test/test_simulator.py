import unittest
import simulator
import messaging
import mock
import datetime
import asyncio
from unittest.mock import ANY


async def publish(*args):
    return await simulator.publish_value(*args)


class TestSimulator(unittest.TestCase):

    @mock.patch("simulator.MessageProducer")
    def test_publish_value(self, producer_mock):
        with mock.patch("profiles.profile.Profile") as profile_mock:
            get_value_at_time_mock = mock.Mock()
            get_value_at_time_mock.return_value = (1234, "W")
            profile_mock.return_value = mock.Mock(get_value_at_time=get_value_at_time_mock, TYPE="Profile")

            producer_mock.get_instance = mock.MagicMock()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                simulator.publish_value(False, "my_device", profile_mock, 2, datetime.datetime(2020, 10, 20, 20, 11, 12)))
            loop.close()
            producer_mock.get_instance().publish.assert_called_once_with(ANY, queue='meter_load')

