from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView

from Users.models import User
from .forms import CustomUserCreationForm, VerifyForm, ResetPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .verify import send, check, sms_reset
from django.contrib.auth import get_user_model
from random import randint
# Create your views here.

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@login_required
def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data.get('phone'))
            send(form.cleaned_data.get('phone'))
            return redirect('users:verify', username=form.cleaned_data.get('username'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def verify_code(request, username):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        user = get_object_or_404(get_user_model(), username=username)
        if form.is_valid():
            code = str(form.cleaned_data.get('code'))
            phone = str(user.phone)
            print(phone, "phone")
            print(code)
            if check(phone, code):
                print("ina shigowa nan")
                user.is_verified = True
                user.save()
                return redirect('login')
            else:
                return render(request, 'registration/verify.html', {'form': form, "error": "Invalid Code"})
    else:
        form = VerifyForm()
    return render(request, 'registration/verify.html', {'form': form})


def send_reset_code(request):
        if request.method == "POST":
            form = ResetPasswordForm(data=request.POST)
            if form.is_valid():
                phone = form.cleaned_data.get('phone') #get the phone number
                if User.objects.filter(phone=phone).exists(): #validate if it exist
                    user = get_object_or_404(get_user_model(), phone=phone) 
                    send(phone) #send the verification code to the phone number
                    return redirect('users:verify', username=user.username) #redirect to verify 
                return render(request, 'registration/password_reset.html', {"form": form, 
                "error": "this number isn't registered"})
        else:
            form = ResetPasswordForm()
            return render(request, 'registration/password_reset.html', {"form": form})


def reset_password(request):
    if request.method == "POST":
        form = VerifyForm(data=request.POST)
        if form.is_valid():
            #get the inputted code
            #compare it with the one on the database
            #if they match:
                #redirect a user to a page where he can assign new password
            #if not:
               #tell the user that its not the correct code
    #render the form 
            pass