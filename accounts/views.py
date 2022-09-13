from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from extensions.utils import generate_otp
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from . import forms
from .models import CustomUser


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form_data = form.cleaned_data
        CustomUser.objects.create_user(**form_data)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_phone_verified:
                return redirect('home:index')
            return redirect('accounts:phone_verifaction')
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
            return redirect("accounts:user_panel")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_phone_verified:
                return redirect('home:index')
            return redirect('accounts:phone_verifaction')
        return super().get(request, *args, **kwargs)


@login_required
def phone_verifaction_page(request):
    if request.user.is_phone_verified:
        return redirect("accounts:user_panel")
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)
        phone = request.POST.get("phone")
        otp_code = request.POST.get("otp_code")
        if user.phone == phone and user.otp_code == otp_code:
            user.is_phone_verified = True
            user.save()
            return redirect('accounts:user_panel')
        user.is_phone_verified = False
        user.save()
        return render(request, 'accounts/phone-verifaction.html', {"is_phone_verify": False})
    context = {
        "is_phone_verify": True
    }
    return render(request, 'accounts/phone-verifaction.html', context)


@login_required
def send_otp_code(request):
    if request.method == "POST":
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


@login_required
def user_panel_page(request):
    if not request.user.is_phone_verified:
        return redirect('accounts:phone_verifaction')
    context = {}
    return render(request, 'accounts/user-panel.html', context)


@login_required
def edit_user_profile_page(request):
    if not request.user.is_phone_verified:
        return redirect('accounts:phone_verifaction')
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        image = request.FILES.get("profile-image")
        print(image)
        obj, created = CustomUser.objects.update_or_create(id=request.user.id, defaults={
            'fullname': fullname,
            'phone': phone,
            'email': email,
            'image': image,
        },)
        return redirect('accounts:edit_profile')
    context = {}
    return render(request, 'accounts/edit-user-panel.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('home:index')


def forgot_password_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email=email.lower()).first()
        if not user:
            return render(request, 'accounts/forgot-password.html', {"email_not_exists": True})
        return render(request, 'accounts/forgot-password.html', {"email_send": True})
    return render(request, 'accounts/forgot-password.html')


def reset_password_page(request):
    return render(request, 'accounts/reset-password.html')
