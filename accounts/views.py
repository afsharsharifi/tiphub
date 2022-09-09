from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from extensions.utils import generate_otp

from . import forms
from .models import CustomUser

# Create your views here.


def register_page(request):
    if request.user.is_authenticated:
        if request.user.is_phone_verified:
            return redirect('accounts:user_panel')
        return redirect('accounts:phone_verifaction')
    register_form = forms.RegisterForm(request.POST or None)
    if register_form.is_valid():
        fullname = register_form.cleaned_data.get('fullname')
        phone = register_form.cleaned_data.get('phone')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        CustomUser.objects.create_user(fullname=fullname, email=email, phone=phone, password=password)
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:phone_verifaction')

    context = {
        'register_form': register_form,
    }
    return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_phone_verified:
            return redirect('accounts:user_panel')
        return redirect('accounts:phone_verifaction')
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        phone = login_form.cleaned_data.get('phone')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect("accounts:user_panel")
    context = {
        'login_form': login_form,
    }
    return render(request, 'accounts/login.html', context)


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
