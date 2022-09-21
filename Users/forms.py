from dataclasses import fields
from pyexpat import model
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import SelectDateWidget

from .models import User


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, help_text='Phone number')

    class Meta:
        model = User
        fields = ("username", "first_name", "middle_name", "last_name", "phone")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "middle_name", "last_name", "phone")


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
        'image', 'first_name', 'middle_name', 'last_name', 'email', 'date_of_birth', 'phone', 'state', 'occupation')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"))
        self.fields['image'].widget.attrs['class'] = 'form-input'
        self.fields['first_name'].widget.attrs['class'] = 'form-input'
        self.fields['middle_name'].widget.attrs['class'] = 'form-input'
        self.fields['last_name'].widget.attrs['class'] = 'form-input'
        self.fields['email'].widget.attrs['class'] = 'form-input'
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-input'
        self.fields['phone'].widget.attrs['class'] = 'form-input'
        self.fields['state'].widget.attrs['class'] = 'form-input'
        self.fields['occupation'].widget.attrs['class'] = 'form-input'


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image', 'date_of_birth']

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')


class SendResetCodeForm(forms.Form):
    phone = forms.CharField(max_length=20, required=True, help_text='Phone number')


class ResetPawsswordForm(forms.Form):
    password1 = forms.CharField(max_length=128)
    password2 = forms.CharField(max_length=128)


class KYCVerifyForm(ModelForm):
    class Meta:
        model = User
        fields = ("address", "bvn", "nin",
                  "time_in_business", "sector", "size", "number_of_employee")

    def __init__(self, *args, **kwargs):
        super(KYCVerifyForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'form-input'
        self.fields['bvn'].widget.attrs['class'] = 'form-input'
        self.fields['nin'].widget.attrs['class'] = 'form-input'
        self.fields['time_in_business'].widget.attrs['class'] = 'form-input'
        self.fields['sector'].widget.attrs['class'] = 'form-input'
        self.fields['size'].widget.attrs['class'] = 'form-input'
        self.fields['number_of_employee'].widget.attrs['class'] = 'form-input'