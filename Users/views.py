from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def education(request):
    return render(request, "education.html")

def chating(request):
    return render(request, "chat.html")

def conversation(request):
    return render(request, "conversations.html")