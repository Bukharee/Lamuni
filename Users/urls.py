from django.urls import path
from .views import index, education

urlpatterns = [
    path("", index, name="index"),
    path("education/", education, name="education"),
    ]
