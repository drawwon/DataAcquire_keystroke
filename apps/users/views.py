from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import UserProfile,EmailVerifyRecord

from django.views.generic.base import View
from users.forms import LoginForm,RegisterForm,ForgetPwdForm,ResetPwdForm,PcFrom

from django.contrib.auth.hashers import make_password
import json
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            request.session['username'] = user_name
            request.session.set_expiry(60000)
            user = authenticate(username=user_name,password=pass_word)
            if user:
                login(request, user)
                return render(request, 'index.html',{'userprofile':user})
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误'})
        else:
            return render(request,'login.html',{'login_form':login_form})

class MoboileDataView(View):
    def get(self, request):
        return render(request, 'mobile_data.html', {})

class PcDataMouseView(View):
    def get(self, request):
        return render(request, 'pc_data_mouse.html', {})

class PcDataView(View):
    def get(self, request):
        return render(request, 'pc_data.html', {})
    def post(self, request):
        # user_name = request.POST.get('username')
        # pass_word = request.POST.get('password')
        body = json.loads(request.body)
        user_name = body['username']
        pass_word = body['password']
        user = authenticate(username=user_name, password=pass_word)
        if user:
            return HttpResponse('true')
        else:
            return HttpResponse('false')
        # pc_form = PcFrom(request.POST)
        # if pc_form.is_valid():
        #     user_name = request.POST.get('username','')
        #     pass_word = request.POST.get('password','')
        #     user = authenticate(username=user_name,password=pass_word)
        #     if user:
        #         return render(request, 'pc_data.html',{'if_true':'true'})
        #     else:
        #         return render(request,'pc_data.html',{'msg':'用户名或密码错误'})
        # else:
        #     return render(request,'pc_data.html',{'pc_form':pc_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            gender =request.POST.get('gender','')
            age = request.POST.get('age', '')
            is_used = UserProfile.objects.filter(email=user_name)
            if not is_used:
                user = UserProfile()
                user.username = user_name
                user.email = user_name
                user.password = make_password(pass_word)
                user.gender = gender
                user.age = age
                user.save()
                send_register_email(user_name)
                return render(request, 'login.html',{})
            else:
                return render(request, 'register.html', {'msg':'该用户名已经被占用','register_form':register_form})
        else:
            return render(request, 'register.html',{'register_form':register_form})



class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')

class ForgetPwdView(View):
    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_pwd_form':forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get('email','')
            if UserProfile.objects.filter(email=email):
                send_register_email(email,send_type=1)
                return render(request,'send_success.html')
            else:
                return render(request,'forgetpwd.html',{'msg':'用户名不存在','forget_pwd_form':forget_pwd_form})
        else:
            return render(request,'forgetpwd.html',{'forget_pwd_form':forget_pwd_form})

class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                return render(request, 'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')

class ModifyPwdView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            pw1 = request.POST.get('password1','')
            pw2 = request.POST.get('password2','')
            email = request.POST.get('email', '')
            if pw1 != pw2:
                return render(request,'password_reset.html',{'msg':"两次密码不一致"})
            else:
                user = UserProfile.objects.get(email=request.POST.email)
                user.password = make_password(pw1)
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'reset_form':reset_form,'email':request.POST.email})

from django.contrib.auth import logout
def logout_view(request):
    logout(request)