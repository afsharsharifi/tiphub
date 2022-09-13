from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from extensions.utils import generate_otp
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView, UpdateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

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
            return redirect('accounts:user_panel')
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


class UserPanelView(View):
    template_name = 'accounts/user-panel.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_phone_verified:
            return redirect('accounts:phone_verifaction')
        return render(request, self.template_name)


class EditUserProfileView(View):
    template_name = "accounts/edit-user-panel.html"

    def get(self, request, *args, **kwargs):
        form = forms.EditUserProfileForm(instance=request.user)
        return render(request, 'accounts/edit-user-panel.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.EditUserProfileForm(request.POST, request.FILES, instance=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponse("Form Saved")
        return HttpResponse("Form is not valid")
        # fullname = request.POST.get("fullname")
        # phone = request.POST.get("phone")
        # email = request.POST.get("email")
        # image = request.FILES.get("profile-image")
        # CustomUser.objects.filter(id=self.request.user.id).update(
        #     fullname=fullname,
        #     phone=phone,
        #     email=email,
        #     image=image,
        # )
        # obj, created = CustomUser.objects.update_or_create(id=request.user.id, defaults={
        #     'fullname': fullname,
        #     'phone': phone,
        #     'email': email,
        #     'image': image,
        # },)
        return redirect('accounts:edit_profile')


# @login_required
# def edit_user_profile_page(request):
#     if not request.user.is_phone_verified:
#         return redirect('accounts:phone_verifaction')
#     if request.method == "POST":
#         fullname = request.POST.get("fullname")
#         phone = request.POST.get("phone")
#         email = request.POST.get("email")
#         image = request.FILES.get("profile-image")
#         print(image)
#         obj, created = CustomUser.objects.update_or_create(id=request.user.id, defaults={
#             'fullname': fullname,
#             'phone': phone,
#             'email': email,
#             'image': image,
#         },)
#         return redirect('accounts:edit_profile')
#     context = {}
#     return render(request, 'accounts/edit-user-panel.html', context)


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
