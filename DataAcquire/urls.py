"""DataAcquire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path,include
from django.views.generic import TemplateView
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,PcDataView,PcDataMouseView
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import logout
from auth_server.views import register_keystroke



urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    re_path(r'^register/', RegisterView.as_view(), name='register'),
    re_path(r'^login/', LoginView.as_view(), name='login'),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^pc_data_keystroke/$',PcDataView.as_view(),name='pc_data'),
    url(r'^pc_data_mouse/$',PcDataMouseView.as_view(),name='pc_data_mouse'),

    url(r'^server/register_keystroke/$',register_keystroke,name='register_keystroke')
]
