from django.urls import path
from .views import index, singup, login, education

app_name = "users"

urlpatterns = [path("", index, name="index"),
               path("login/", login, name="login"),
               path("signup/", singup, name="signup")
               path("education/", education, name="education"),
               ]


