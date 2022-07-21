from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")


def singup(request):
    return render(request, "signup.html")


def blog(request):
    return render(request, "blog-detail.html")

def education(request):
    return render(request, "education.html")


def quiz(request):
    return render(request, "quiz.html")


