from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserPanelView.as_view(), name="user_panel"),
    path('edit/', views.EditUserProfileView.as_view(), name="edit_profile"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('phone-verifaction/', views.PhoneVerifactionView.as_view(), name="phone_verifaction"),
    path('phone-verifaction/send-otp/', views.SendOTPView.as_view(), name="send_otp_code"),
    path('password-change/', views.PasswordChangeView.as_view(), name="password_change"),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    # All Working Until Here
    path('password-reset/', views.PasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset/reset/done/', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
