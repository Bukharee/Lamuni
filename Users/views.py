from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from requests import request
from Wallet.models import Wallet

from Users.models import User
from Loans.models import Loan, Beneficiaries
from .forms import CustomUserCreationForm, VerifyForm, SendResetCodeForm, ResetPawsswordForm, UserEditForm
from django.contrib.auth.decorators import login_required
from .verify import send, check, sms_reset
from django.contrib.auth import get_user_model
from Wallet.models import Wallet, Transaction


# Create your views here.


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
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


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


def lesson_detail(request):
    return render(request, "lesson-detail.html")


def lesson_done(request):
    return render(request, "lesson-done.html")


def education(request):
    return render(request, "education.html")


def chating(request):
    return render(request, "chat.html")


def conversation(request):
    return render(request, "conversations.html")
    return render(request, "education_base.html")


def send_reset_code(request):
    if request.method == "POST":
        form = SendResetCodeForm(data=request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')  # get the phone number
            if User.objects.filter(phone=phone).exists():  # validate if it exist
                user = get_object_or_404(get_user_model(), phone=phone)
                send(phone)  # send the verification code to the phone number
                return redirect('users:reset_verify', username=user.username)  # redirect to verify
            return render(request, 'registration/password_reset.html', {"form": form,
                                                                        "error": "this number isn't registered"})
    else:
        form = SendResetCodeForm()
        return render(request, 'registration/password_reset.html', {"form": form})


def quiz(request):
    return render(request, "quiz.html")


def quiz_result(request):
    return render(request, "quiz-result.html")


def reset_verify(request, username):
    if request.method == "POST":
        user = get_object_or_404(get_user_model(), username=username)
        form = VerifyForm(data=request.POST)
        if form.is_valid():
            code = str(form.cleaned_data.get('code'))  # get the inputted code
            # compare it with the one sent
            if check(user.phone, code):  # if they match:
                user.reset_code = code
                user.save()
                return redirect('users:reset_password', username=user.username,
                                code=code)  # redirect a user to a page where he can assign new password
            return render(request, 'registration/reset_code_verify.html', {"form": form,
                                                                           "error": "invalid code"})  # if not: tell the user that its not the correct code
    form = VerifyForm()
    return render(request, "registration/reset_code_verify.html", {"form": form})
    # render the form


def reset_password(request, username, code):
    user = get_object_or_404(get_user_model(), username=username)
    if user.reset_code == str(code):
        print("code matched")
        if request.method == "POST":
            form = ResetPawsswordForm(data=request.POST)
            if form.is_valid():
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                if password1 == password2:
                    user.set_password(password1)
                    authenticate(username=user.username, password=password1)
                    user.reset_code = ""
                    user.save()
                    return redirect('users:index')
                return render(request, 'registration/password_reset_temp.html',
                              {"form": form, "error": "passwords dont match"})
        form = ResetPawsswordForm()
        return render(request, 'registration/password_reset_temp.html', {"form": form})
    return render(request, 'registration/resend_code_error.html', {"error": "oops!, go get a reset code first!"})


@login_required
def user_profile(request):
    user = request.user

    try:
        wallet = Wallet.objects.get(owner=user)

    except Exception:

        wallet = Wallet.objects.create(
            owner=user,
            owner_type="User", )

    transactions1 = Transaction.objects.filter(receiver=user)
    transactions2 = Transaction.objects.filter(sender=user)

    transactions = transactions1 | transactions2
    loans_applied = Beneficiaries.objects.filter(user=user)
    number_of_loan_applied = Beneficiaries.objects.filter(user=user).count()

    context = {'user': user, 'wallet': wallet, 'transactions': transactions}

    return render(request, 'profile.html', context)


def update_user_profile(request):
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Has Been Updated')
            return redirect('users:profile')
        else:
            print(form.errors)
    else:
        form = UserEditForm(instance=request.user)
        print(form)
    return render(request, 'edit_profile.html', {'form': form})


def financial_statement(request):
    return render(request, "financial-statement.html")
