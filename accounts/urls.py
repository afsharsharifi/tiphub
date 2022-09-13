from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path('', views.UserPanelView.as_view(), name="user_panel"),
    path('edit', views.EditUserProfileView.as_view(), name="edit_profile"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('phone-verifaction', views.PhoneVerifactionView.as_view(), name="phone_verifaction"),
    path('phone-verifaction/send-otp', views.SendOTPView.as_view(), name="send_otp_code"),
    path('forgot-password', views.forgot_password_page, name="forgot_password"),
    path('reset-password', views.reset_password_page, name="reset_password"),
]
