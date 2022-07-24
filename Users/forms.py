from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, help_text='Phone number')

    class Meta:
        model = User
        fields = ("username", "name", "phone")


class CustomUserChangeForm(UserChangeForm):
    
        
    class Meta:
        model = User
        fields = ("username", "name", "phone")

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

class SendResetCodeForm(forms.Form):
        phone = forms.CharField(max_length=20, required=True, help_text='Phone number')

class ResetPawsswordForm(forms.Form):
        password1 = forms.CharField(max_length=128)
        password2 = forms.CharField(max_length=128)

