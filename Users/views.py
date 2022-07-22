from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")


def singup(request):
    return render(request, "signup.html")


def lesson_detail(request):
    return render(request, "blog-detail.html")

def lesson_done(request):
    return render(request, "lesson-done.html")

def education(request):
    return render(request, "education.html")

def quiz(request):
    return render(request, "quiz.html")

def quiz_result(request):
    return render(request, "quiz-result.html")



