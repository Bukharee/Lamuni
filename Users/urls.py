from django.urls import path
from .views import index, education, chating, conversation

urlpatterns = [
    path("", index, name="index"),
    path("education/", education, name="education"),
    path("bot/", chating, name="bot"),
    path("conversation/", conversation, name="conversation"),
    ]
