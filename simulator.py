from datetime import datetime, timedelta
import asyncio
import json
from utils import round_time
from profiles.profile import *
from messaging.producer import MessageProducer
from messaging.constants import *


PROFILE_CLASS = {"LoadProfile": LoadProfile, "PvProfile": PvProfile}
event_loop = asyncio.get_event_loop()


async def publish_value(device, profile_class, freq, start_time):
    loop_start_time_utc = datetime.utcnow()
    profile_class_object = profile_class()
    while True:
        await asyncio.sleep(freq)
        current_time_utc = datetime.utcnow()
        seconds_elapsed = int((current_time_utc - loop_start_time_utc).total_seconds())
        required_timestamp = round_time(start_time + timedelta(seconds=seconds_elapsed))
        value, unit = profile_class_object.get_value_at_time(required_timestamp)
        msg = json.dumps({"timestamp": required_timestamp.strftime("%Y-%m-%d %H:%M:%S"), "value": value,
                          "device": device, "unit": unit, "payload_type": profile_class().TYPE })
        MessageProducer().publish(msg, queue=SIMULATOR_QUEUE)
        print("Published {} for {} with frequency {}".format(msg, profile_class, freq))
        return


def start(profile_details):
    try:
        for profile in profile_details:
            freq = profile.get('freq', 60)
            start_time = profile.get('start_time', datetime.utcnow())
            device = profile.get('device_identifier', None)
            asyncio.ensure_future(publish_value(device, PROFILE_CLASS[profile['profile']], freq, start_time))
        event_loop.run_forever()
    except KeyboardInterrupt:
        event_loop.stop()
    except Exception as e:
        raise e
    finally:
        print("Closing Loop")
        event_loop.close()


def stop():
    try:
        event_loop.stop()
    finally:
        event_loop.close()
