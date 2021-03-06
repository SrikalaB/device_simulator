import profiles.constants as ProfileConstants
import csv


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

    def _build_from_csv_file(self):
        """
        Opens CSV mentioned in file path creates a dictionary with key as time and value as profile's reading
        Example entry:
          {"01:10:20": (1230, W)}
          At 1 o clock 10 mins and 20 seconds the device's instantaneous reading is 1230 Watts
        :return:
        """
        try:
            _profile_dict = {}
            csv_file = open(self.file_path, 'r')
            reader = csv.reader(csv_file)
            next(reader) # Skip header
            for row in reader:
                time, value, unit = row
                value = float(value)
                _profile_dict[time] = (value, unit)
            csv_file.close()
            return _profile_dict
        except OSError as e:
            print("Could not open/read file:", self.file_path)
            raise e

    def _get_profile(self):
        if not self.profile:
            self.profile = self._build_from_csv_file()
        return self.profile

    def get_value_at_time(self, timestamp, desired_unit=ProfileConstants.WATTS):
        try:
            value, unit = self._get_profile()[timestamp.strftime('%H:%M:%S')]
            if unit == desired_unit:
                return value, unit
            elif unit == ProfileConstants.WATTS and desired_unit == ProfileConstants.KILO_WATTS:
                return value/1000, desired_unit
        except Exception as e:
            print("Unable to generate value for given timestamp")


class LoadProfile(Profile):
    TYPE = "meter_data"

    def __init__(self, **kwargs):
        Profile.__init__(self, **kwargs)
        self.file_path = kwargs.get('file_path', ProfileConstants.METER_PROFILE_24H_FILEPATH)


class PvProfile(Profile):
    TYPE = "PV_data"

    def __init__(self, **kwargs):
        Profile.__init__(self, **kwargs)
        self.file_path = kwargs.get('file_path', ProfileConstants.PV_PROFILE_24H_FILEPATH)

