from django import forms
from django.contrib.auth.models import User
from django.core import validators


class RegisterForm(forms.Form):
    fullname = forms.CharField()
    phone = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
