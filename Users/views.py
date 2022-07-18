from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
# Create your views here.

def index(request):
    return render(request, "index.html")


def singup(request):
    return render(request, "registration/signup.html")


def blog(request):
    return render(request, "blog-detail.html")

def education(request):
    return render(request, "education.html")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"