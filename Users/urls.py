from django.urls import path
from .views import index, singup, login, education, blog, quiz

app_name = "users"

urlpatterns = [
    path("", index, name="index"),
               path("login/", login, name="login"),
               path("signup/", singup, name="signup"),
               path("blog/", blog, name="blog"),
               path("education/", education, name="education"),
    path("quiz/", quiz, name="quiz")
]

