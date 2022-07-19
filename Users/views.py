from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, VerifyForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .verify import send, check
from django.contrib.auth import get_user_model
# Create your views here.

@login_required
def index(request):
    return render(request, "index.html")


def blog(request):
    return render(request, "blog-detail.html")

def education(request):
    return render(request, "education.html")


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