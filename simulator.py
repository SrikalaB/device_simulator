from datetime import datetime, timedelta
import asyncio
import json
from utils import round_time
from profiles.profile import *
from messaging.producer import MessageProducer
from messaging.constants import *


PROFILE_CLASS = {"LoadProfile": LoadProfile, "PvProfile": PvProfile}
event_loop = asyncio.get_event_loop()


async def publish_value(run_indefinitely, device, profile_class, freq, start_time):
    """
    Gets value from profile_class at a given instant of time and called publisher to publish json message
    :param run_indefinitely Indicates whether a infinite while loop is required
    :param device: string. Identifier of the device for which we are creating the profile
    :param profile_class: type. Class which corresponds to the profile being generated
    :param freq: int. Frequency in seconds at which the message should be published
    :param start_time: datetime. Date and time at which the timestamp in published messages should start.
    :return:
    """
    loop_start_time_utc = datetime.utcnow()
    profile_class_object = profile_class()
    to_run = True
    while to_run:
        current_time_utc = datetime.utcnow()
        seconds_elapsed = int((current_time_utc - loop_start_time_utc).total_seconds())
        required_timestamp = round_time(start_time + timedelta(seconds=seconds_elapsed))
        value, unit = profile_class_object.get_value_at_time(required_timestamp)
        msg = json.dumps({"timestamp": required_timestamp.strftime("%Y-%m-%d %H:%M:%S"), "value": value,
                          "device": device, "unit": unit, "payload_type": profile_class().TYPE })
        producer = MessageProducer.get_instance()
        producer.publish(msg, queue=SIMULATOR_QUEUE)
        print("Published {} for {} with frequency {}".format(msg, profile_class.__name__, freq))
        await asyncio.sleep(freq)
        if not run_indefinitely:
            return


def start(profile_details):
    """
    Starts simulation for all profiles passed
    :param profile_details: List of dictionaries. Each dictionary contains information about the simulation to run.
                            The keys allowed are
                            "freq" - To denote frequency.
                            "profile" - Class name of the profile to be simulated
                            "device_identifier" - Name of the device being simulated
                            "start_time" - UTC time at which the generator should start the first value
    """
    try:
        for profile in profile_details:
            freq = profile.get('freq', 60)
            start_time = profile.get('start_time', datetime.utcnow())
            device = profile.get('device_identifier', None)
            event_loop.create_task(publish_value(True, device, PROFILE_CLASS[profile['profile']], freq, start_time))
        event_loop.run_forever()
    except KeyboardInterrupt:
        event_loop.stop()
    except Exception as e:
        raise e
    finally:
        print("Closing Loop")
        event_loop.close()
