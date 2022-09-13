from django import forms
from django.core import validators
from django.contrib.auth import authenticate
from .models import CustomUser


class RegisterForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'نام و نام خانوادگی',
                'class': 'email-input',
                'dir': 'rtl',
            },
        ),
        label='نام و نام خانوادگی',
        validators=[
            validators.MaxLengthValidator(150, 'نام و نام خانوادگی نمیتواند بیشتر از 150 کاراکتر باشد')
        ]
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'شماره تلفن',
                'class': 'email-input',
                'dir': 'ltr',
                'maxlength': '11',
            }
        ),
        label='شماره تلفن',
        validators=[
            validators.MaxLengthValidator(11, 'شماره تلفن باید 11 کاراکتر باشد'),
            validators.MinLengthValidator(11, 'شماره تلفن باید 11 کاراکتر باشد'),
        ]
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'پست الکترونیک',
                'class': 'email-input',
                'dir': 'ltr',
            }
        ),
        label='پست الکترونیک',
        validators=[
            validators.EmailValidator('ایمیل وارد شده صحیح نیست')
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'گذزواژه',
                'class': 'password-input',
                'dir': 'ltr',
            }
        ),
        label='گذرواژه',
        validators=[
            validators.MinLengthValidator(8, 'گذرواژه باید بیشتر از 8 کاراکتر باشد')
        ]
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        is_email_exists = CustomUser.objects.filter(email=email.lower()).exists()

        if is_email_exists:
            raise forms.ValidationError('کاربری با این ایمیل وجود دارد')
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        is_phone_exists = CustomUser.objects.filter(phone=phone).exists()
        if is_phone_exists:
            raise forms.ValidationError('کاربری با این شماره تلفن وجود دارد')
        return phone


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'شماره تلفن',
                'class': 'email-input',
                'dir': 'ltr',
                'maxlength': '11',
            }
        ),
        label='شماره تلفن',
        validators=[
            validators.MaxLengthValidator(11, 'شماره تلفن باید 11 کاراکتر باشد'),
            validators.MinLengthValidator(11, 'شماره تلفن باید 11 کاراکتر باشد'),
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'گذزواژه',
                'class': 'password-input',
                'dir': 'ltr',
            }
        ),
        label='گذرواژه',
    )

    def clean(self):
        user = authenticate(username=self.cleaned_data.get("username"), password=self.cleaned_data.get("password"))
        if user is None:
            raise forms.ValidationError("گذزواژه یا شماره تلفن اشتباه است", code="invalid_information")
