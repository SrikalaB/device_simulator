import profiles.constants as ProfileConstants
from datetime import datetime
import csv
import pandas as pd


class Profile:
    def __init__(self, file_path=None, scale_factor=1):
        self.scale = scale_factor
        self.file_path = file_path
        self.profile = {}

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        """
        Required param
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Scaling factor can only be a numeric value")
        self._scale = value

    def build_from_csv_file(self):
        try:
            _profile_dict = {}
            reader = csv.reader(open(self.file_path, 'r'))
            for row in reader:
                time, value = row
                _profile_dict[time] = value
            return _profile_dict
        except OSError as e:
            print("Could not open/read file:", self.file_path)
            raise e

    def get_value_at_time(self, timestamp):
        try:
            if not self.profile:
                self.profile = self.build_from_csv_file()
            return self.profile[timestamp.strftime('%H:%M:%S')]
        except Exception as e:
            print("Unable to generate value for given timestamp")


class LoadProfile(Profile):

    def __init__(self, **kwargs):
        Profile.__init__(self, **kwargs)
        self.file_path = kwargs.get('file_path', ProfileConstants.METER_PROFILE_24H_FILEPATH)


class PvProfile(Profile):

    def __init__(self, **kwargs):
        Profile.__init__(self, **kwargs)
        self.file_path = kwargs.get('file_path', ProfileConstants.PV_PROFILE_24H_FILEPATH)

