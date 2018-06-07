import json

import numpy as np

from auth_server.models import KeyStroke
from .keystroke_factory import KeyStrokeFactory


class KeyStrokeManager:
    REGISTRATION_SAMPLES_COUNT = 2
    KEYSTROKE_MIN_COINCIDENCE = 0.8

    def __init__(self, user):
        self.user = user
        self.factory = KeyStrokeFactory(user)

    def get_keystrokes(self, is_temporary):
        return KeyStroke.objects.filter(user=self.user, is_temporary=is_temporary).all()


    def get_keystrokes_count(self, is_temporary):
        """
        :param is_temporary:
        :return:
        """
        login_keystrokes_count = KeyStroke.objects.filter(
            user=self.user, is_temporary=is_temporary, type=KeyStroke.LOGIN_TYPE
        ).count()

        password_keystrokes_count = KeyStroke.objects.filter(
            user=self.user, is_temporary=is_temporary, type=KeyStroke.PASSWORD_TYPE
        ).count()
        return min(login_keystrokes_count, password_keystrokes_count)

    def delete_keystrokes(self, is_temporary):
        user_keystrokes = KeyStroke.objects.filter(user=self.user, is_temporary=is_temporary).all()
        if user_keystrokes:
            user_keystrokes.delete()

    def authenticate(self, login_timestamps, password_timestamps):
        user_login_keystroke = self.user.keystroke_set.filter(is_temporary=False, type=KeyStroke.LOGIN_TYPE).first()
        user_password_keystroke = self.user.keystroke_set.filter(is_temporary=False, type=KeyStroke.PASSWORD_TYPE).first()

        login_keystroke_to_authenticate = self.factory.create_from_timestamps(login_timestamps, without_save=True)
        password_keystroke_to_authenticate = self.factory.create_from_timestamps(password_timestamps, without_save=True)

        login_coincidence = self.__get_keystroke_coincidence(user_login_keystroke, login_keystroke_to_authenticate)
        password_coincidence = self.__get_keystroke_coincidence(user_password_keystroke, password_keystroke_to_authenticate)
        is_valid_keystroke = self.__is_valid_coincidence(login_coincidence, password_coincidence)
        return {
            'login': login_coincidence,
            'password': password_coincidence,
            'is_valid_keystroke': is_valid_keystroke,
            'message': 'Auth result: {0}. Metrics: login - {1}, {2}; password - {3}, {4}'.format(
                'authenticated' if is_valid_keystroke else 'not authenticated',
                login_coincidence['dwell_coincidence'],
                login_coincidence['flight_coincidence'],
                password_coincidence['dwell_coincidence'],
                password_coincidence['flight_coincidence'],
            )
        }

    def __is_valid_coincidence(self, login_coincidence, password_coincidence):
        mean_login = np.mean([login_coincidence['dwell_coincidence'], login_coincidence['flight_coincidence']])
        mean_password = np.mean([password_coincidence['dwell_coincidence'], password_coincidence['flight_coincidence']])
        return mean_login >= self.KEYSTROKE_MIN_COINCIDENCE and mean_password >= self.KEYSTROKE_MIN_COINCIDENCE

    def __get_keystroke_coincidence(self, keystroke_a, keystroke_b):
        dwell_coincidence = self.__get_mean_deviation(
            json.loads(keystroke_a.dwell_times),
            json.loads(keystroke_b.dwell_times)
        )
        flight_coincidence = self.__get_mean_deviation(
            json.loads(keystroke_a.flight_times),
            json.loads(keystroke_b.flight_times)
        )
        return {
            'dwell_coincidence': dwell_coincidence,
            'flight_coincidence': flight_coincidence,
        }

    @staticmethod
    def __get_mean_deviation(list_a, list_b):
        if not len(list_a) == len(list_b):
            return 0
        coincidences = []
        for i in range(len(list_a)):
            coincidence = 1 - (abs(list_a[i] - list_b[i]) / list_a[i])
            coincidences.append(coincidence)

        return round(sum(coincidences)/len(coincidences), 2)
