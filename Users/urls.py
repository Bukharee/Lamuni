from django.urls import path
from .views import index, singup, login, blog
app_name = "users"

urlpatterns = [path("", index, name="index"),
               path("login/", login, name="login"),
               path("signup/", singup, name="signup"),
               path("blog/", blog, name="blog")
               ]

