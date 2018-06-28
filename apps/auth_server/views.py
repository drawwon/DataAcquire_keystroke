from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json,re
from auth_server.models import KeyStroke,Mouse,MobileData

from utils.response_statuses import RESPONSE,RESPONSE_STATUS
from utils.custom_exceptions import InvalidKeystrokeException
from utils.dict_get import dict_get
from users.models import UserProfile as User
from utils.keystroke_manager import KeyStrokeManager


# Create your views here.
def register_keystroke(request):
    # print(bool(re.search('pc_data_keystroke',request.META['HTTP_REFERER'])))
    if re.search('pc_data_keystroke',request.META['HTTP_REFERER']):
        data = json.loads(request.body)
        login, password, login_timestamps, password_timestamps = dict_get(data, 'login', 'password','login_timestamps', 'password_timestamps')
        auth = authenticate(username=login, password=password)
        if not auth:
            return HttpResponse('false')
        else:
            # user = User.objects.get(username=login)
            # print(type(user))
            # keystroke_manager = KeyStrokeManager(user)

            # try:
            #     keystroke_manager.factory.create_temporary_keystrokes_from_timestamps(login_timestamps, password_timestamps)
            # except InvalidKeystrokeException:
            #     return JsonResponse(RESPONSE['INVALID_KEYSTROKE'])

            # temporary_keystrokes_count = keystroke_manager.get_keystrokes_count(is_temporary=True)

            # if temporary_keystrokes_count == 1:
                # return JsonResponse(RESPONSE['NEED_MORE_SAMPLE'])

            # if temporary_keystrokes_count >= KeyStrokeManager.REGISTRATION_SAMPLES_COUNT:
            # keystroke_manager.delete_keystrokes(is_temporary=False)
            # keystroke_manager.factory.create_average_keystrokes()
            # keystroke_manager.delete_keystrokes(is_temporary=True)
            # print("login_timestamps['keydowns']" + str(login_timestamps['keydowns']))
            # print("login_timestamps['keydownsAndUps']"+str(login_timestamps['keydownsAndUps']))
            # print("password_timestamps['keydowns']"+str(password_timestamps['keydowns']))
            # print("password_timestamps['keydownsAndUps']" + str(password_timestamps['keydownsAndUps']))

            user = User.objects.get(username=login)
            keystroke_data = KeyStroke()
            keystroke_data.login_times_keydowns = json.dumps(login_timestamps['keydowns'])
            keystroke_data.login_times_keydowns_and_ups = json.dumps(login_timestamps['keydownsAndUps'])
            keystroke_data.password_times_keydowns = json.dumps(password_timestamps['keydowns'])
            keystroke_data.password_times_keydowns_and_ups = json.dumps(password_timestamps['keydownsAndUps'])
            keystroke_data.type = 1
            keystroke_data.user = user
            keystroke_data.user_name = user.username

            keystroke_data.save()

            return JsonResponse(RESPONSE['SUCCESS'])

    elif re.search('pc_data_mouse',request.META['HTTP_REFERER']):
        data = json.loads(request.body)
        cor_data = data['mouse_xy']
        timestamps = data['timestamps']
        user = User.objects.get(username=request.user.username)

        mouse_data = Mouse()
        mouse_data.user = user
        mouse_data.user_name = user.username
        mouse_data.timestamps = timestamps
        mouse_data.cor_pos = cor_data
        mouse_data.save()
        # user = User.objects.get(username=login)
        return HttpResponse('success')
        # return JsonResponse(RESPONSE['SUCCESS'])
        # return HttpResponse('true')

    elif re.search('mobile_data',request.META['HTTP_REFERER']):
        data = json.loads(request.body)
        user = User.objects.get(username=request.user.username)
        acc_datas = data['acc_datas']
        acc_with_gravitys = data['acc_with_gravitys']
        rot_rates = data['rot_rates']
        acc_angle = data['acc_angle']
        touch_data = data['touch_data']

        print(touch_data)


        mobile_data = MobileData()
        mobile_data.user = user
        mobile_data.user_name = user.username

        mobile_data.touch_data = touch_data
        mobile_data.acc_datas = acc_datas
        mobile_data.acc_with_gravitys = acc_with_gravitys
        mobile_data.rot_rates = rot_rates
        mobile_data.acc_angle = acc_angle

        mobile_data.save()
        return HttpResponse('success')


    else:
        return HttpResponse('false')


        # return JsonResponse(RESPONSE['NEED_MORE_SAMPLE'])