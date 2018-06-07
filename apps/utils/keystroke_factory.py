import json

import numpy as np

from utils.frontend import FRONTEND_FIELDS
from auth_server.models import KeyStroke
from utils.custom_exceptions import InvalidKeystrokeException


class KeyStrokeFactory:
    MAXIMUM_FLIGHT_TIME = 825
    MAXIMUM_DWELL_TIME = 200

    def __init__(self, user):
        self.user = user

    def create(self, flight_times, dwell_times, **kwargs):
        return KeyStroke.objects.create(
            user = self.user,
            flight_times=json.dumps(flight_times),
            dwell_times=json.dumps(dwell_times),
            **kwargs
        )

    @staticmethod
    def create_without_save(flight_times, dwell_times, **kwargs):
        return KeyStroke(
            flight_times=json.dumps(flight_times),
            dwell_times=json.dumps(dwell_times),
            **kwargs
        )

    def create_from_timestamps(self, timestamps, without_save=False, **kwargs):
        key_downs, key_downs_and_ups = timestamps[FRONTEND_FIELDS['KEY_DOWNS']], timestamps[FRONTEND_FIELDS['KEY_DOWNS_AND_UPS']]
        flight_times = KeyStrokeFactory.__timestamps_to_flight_times(key_downs)
        self.__check_flight_times(flight_times)

        dwell_times = KeyStrokeFactory.__timestamps_to_dwell_times(key_downs_and_ups)
        self.__check_dwell_times(dwell_times)

        if without_save:
            return self.create_without_save(flight_times, dwell_times, **kwargs)
        return self.create(flight_times, dwell_times, **kwargs)

    def __check_flight_times(self, flight_times):
        error = any(flight_time > self.MAXIMUM_FLIGHT_TIME for flight_time in flight_times)
        if error:
            raise InvalidKeystrokeException()

    def __check_dwell_times(self, dwell_times):
        error = any(dwell_time > self.MAXIMUM_DWELL_TIME for dwell_time in dwell_times)
        if error:
            raise InvalidKeystrokeException()

    def create_average_keystrokes(self):
        self.create_average_keystroke(KeyStroke.LOGIN_TYPE)
        self.create_average_keystroke(KeyStroke.PASSWORD_TYPE)

    def create_average_keystroke(self, keystroke_type):
        temporary_login_keystrokes = KeyStroke.objects.filter(
            user=self.user,
            is_temporary=True,
            type=keystroke_type
        ).all()

        dwell_times = self.__map_key_and_parse('dwell_times', temporary_login_keystrokes)
        average_dwell_times = self.__get_mean_list(dwell_times)

        flight_times = self.__map_key_and_parse('flight_times', temporary_login_keystrokes)
        average_flight_times = self.__get_mean_list(flight_times)
        self.create(
            dwell_times=average_dwell_times,
            flight_times=average_flight_times,
            is_temporary=False,
            type=keystroke_type
        )

    def create_temporary_keystrokes_from_timestamps(self, login_timestamps, password_timestamps):
        self.create_from_timestamps(login_timestamps, type=KeyStroke.LOGIN_TYPE, is_temporary=True)
        self.create_from_timestamps(password_timestamps, type=KeyStroke.PASSWORD_TYPE, is_temporary=True)

    @staticmethod
    def __get_mean_list(lists):
        return np.mean(lists, axis=0).tolist()

    @staticmethod
    def __map_key_and_parse(key, arr):
        return list(map(lambda x: json.loads(getattr(x, key)), arr))

    @staticmethod
    def __timestamps_to_dwell_times(timestamps):
        dwell_count = round(len(timestamps) / 2)
        np_timestamps = np.array(timestamps)
        pairs = np.reshape(np_timestamps, (dwell_count, 2))
        dwells = np.reshape(np.diff(pairs), dwell_count)
        return dwells.tolist()

    @staticmethod
    def __timestamps_to_flight_times(timestamps):
        return np.diff(timestamps).tolist()
