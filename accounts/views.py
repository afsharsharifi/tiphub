from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from .models import CustomUser, Teacher
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404

# Create your views here.


def user_panel_page(request):
    context = {}
    return render(request, 'accounts/user-panel.html', context)


def edit_user_profile_page(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        image = request.FILES.get("profile-image")

        user = CustomUser.objects.filter(id=request.user.id)
        user.update(fullname=fullname, phone=phone, email=email)
        if image:
            user.update(image=image)
        return redirect(reverse('edit_profile'))
    context = {}
    return render(request, 'accounts/edit-user-panel.html', context)


def register_page(request):
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
            return redirect(reverse('index'))

    context = {
        'register_form': register_form,
    }
    return render(request, 'accounts/register.html', context)


def login_page(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        phone = login_form.cleaned_data.get('phone')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('user_panel'))
    context = {
        'login_form': login_form,
    }
    return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect(reverse('index'))


def teacher_profile_page(request, username):
    teacher = get_object_or_404(Teacher, username=username)
    context = {
        'teacher': teacher,
    }
    return render(request, 'accounts/teacher-profile.html', context)


def forgot_password_page(request):
    return render(request, 'accounts/forgot-password.html')


def reset_password_page(request):
    return render(request, 'accounts/reset-password.html')
