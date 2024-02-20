from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']