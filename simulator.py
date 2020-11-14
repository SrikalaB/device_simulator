from datetime import datetime, timedelta
import asyncio
from utils import round_time
from profiles.profile import *


class Simulator(object):
    def __init__(self):
        self.event_loop = asyncio.get_event_loop()

    @classmethod
    async def generate_value(cls, simulation_profile, start_time):
        loop_start_time_utc = datetime.utcnow()
        while True:
            await asyncio.sleep(5)
            current_time_utc = datetime.utcnow()
            seconds_elapsed = int((current_time_utc - loop_start_time_utc).total_seconds())
            required_timestamp = round_time(start_time + timedelta(seconds=seconds_elapsed))
            value = simulation_profile().get_value_at_time(required_timestamp)
            print("Value is {}, {}".format(required_timestamp, value))

    def start(self, profile_classes, start_time=datetime.utcnow()):
        try:
            for profile_cls in profile_classes:
                asyncio.ensure_future(Simulator.generate_value(profile_cls, start_time=start_time))
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            self.event_loop.stop()
        finally:
            print("Closing Loop")
            self.event_loop.close()

    def stop(self):
        try:
            self.event_loop.stop()
        finally:
            self.event_loop.close()
