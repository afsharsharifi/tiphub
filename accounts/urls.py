from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path('', views.user_panel_page, name="user_panel"),
    path('edit', views.edit_user_profile_page, name="edit_profile"),
    path('register', views.register_page, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('phone-verifaction', views.phone_verifaction_page, name="phone_verifaction"),
    path('phone-verifaction/send-otp', views.send_otp_code, name="send_otp_code"),
    path('forgot-password', views.forgot_password_page, name="forgot_password"),
    path('reset-password', views.reset_password_page, name="reset_password"),
]
