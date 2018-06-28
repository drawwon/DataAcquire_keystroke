import xadmin
from xadmin import views
from auth_server.models import MobileData, KeyStroke, Mouse


class BaseSettings:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '西安交大数据采集系统后台管理'
    site_footer = '西安交通大学'
    menu_style = 'accordion'


class MobileDataAdmin:
    list_display = ['user_name', 'acc_with_gravitys', 'rot_rates', 'acc_datas', 'acc_angle', 'touch_data']
    search_fields = ['user_name']
    list_filter = ['user_name']


class KeyStrokeAdmin:
    list_display = ['user_name', 'login_times_keydowns', 'login_times_keydowns_and_ups', 'password_times_keydowns',
                    'password_times_keydowns_and_ups']
    search_fields = ['user_name']
    list_filter = ['user_name']


class MouseAdmin:
    list_display = ['user_name', 'cor_pos', 'timestamps']
    search_fields = ['user_name']
    list_filter = ['user_name']


xadmin.site.register(Mouse, MouseAdmin)
xadmin.site.register(KeyStroke,KeyStrokeAdmin)
xadmin.site.register(MobileData,MobileDataAdmin)

xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)
