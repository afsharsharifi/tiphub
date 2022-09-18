from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView
from extensions.utils import generate_otp

from . import forms
from .mixins import PhoneVerifactionRequiredMixin
from .models import CustomUser


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form_data = form.cleaned_data
        CustomUser.objects.create_user(**form_data)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_phone_verified:
                return redirect('home:index')
            return redirect('phone_verifaction')
        return super().get(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy("home:index")

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = authenticate(self.request, phone=form_data["phone"], password=form_data["password"])
        if user is not None:
            login(self.request, user)
            return redirect("user_panel")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_phone_verified:
                return redirect('home:index')
            return redirect('phone_verifaction')
        return super().get(request, *args, **kwargs)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("home:index")


class PhoneVerifactionView(LoginRequiredMixin, View):
    template_name = 'accounts/phone-verifaction.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_phone_verified:
            return redirect("home:index")
        return render(request, self.template_name, {"is_phone_verify": True})

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=self.request.user.id)
        phone = request.POST.get("phone")
        otp_code = request.POST.get("otp_code")
        if user.phone == phone and user.otp_code == otp_code:
            user.is_phone_verified = True
            user.save()
            return redirect('user_panel')
        user.is_phone_verified = False
        user.save()
        return render(request, self.template_name, {"is_phone_verify": False})


class SendOTPView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        OTP_CODE = generate_otp()
        user = CustomUser.objects.get(id=request.user.id)
        phone = request.POST.get("phone")
        user.phone = phone
        user.otp_code = OTP_CODE
        user.save()
        print(f"OTP Code for {phone} is =>>>>> {OTP_CODE}")
        context = {
            'message': 'Code has been send',
            'status': 200
        }
        return JsonResponse(context)


class UserPanelView(PhoneVerifactionRequiredMixin, View):
    template_name = 'accounts/user-panel.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EditUserProfileView(View):
    template_name = "accounts/edit-user-panel.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_phone_verified:
            return redirect('phone_verifaction')
        form = forms.EditUserProfileForm(instance=request.user)
        return render(request, 'accounts/edit-user-panel.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.EditUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if "phone" in form.changed_data:
                instance.is_phone_verified = False
            if "email" in form.changed_data:
                instance.is_email_verified = False
            instance.save()
            return redirect("edit_profile")
        return render(request, self.template_name)


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "accounts/password_change_form.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/password_reset_form.html"
    success_url = reverse_lazy("password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
