from django.db import models
from users.models import UserProfile as User


# class User(models.Model):
#     login = models.CharField(max_length=200, blank=False)

# Create your models here.
class KeyStroke(models.Model):
    # LOGIN_TYPE = 1
    # PASSWORD_TYPE = 2
    #
    # KEYSTROKE_TYPES = (
    #     (LOGIN_TYPE, 'Login'),
    #     (PASSWORD_TYPE, 'Password'),
    # )

    # flight_times = models.TextField(blank=False)
    # dwell_times = models.TextField(blank=False)
    login_times_keydowns = models.TextField(blank=False)
    login_times_keydowns_and_ups = models.TextField(blank=False)
    password_times_keydowns = models.TextField(blank=False)
    password_times_keydowns_and_ups = models.TextField(blank=False)

    # type = models.IntegerField(choices=KEYSTROKE_TYPES, blank=False)
    is_temporary = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100,blank=True)

class Mouse(models.Model):
    cor_pos = models.TextField(blank=False)
    timestamps = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100,blank=True)

