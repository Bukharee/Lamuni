from django.urls import path
from .views import index, register, education, blog, verify_code
from django.contrib.auth import views as auth_views


app_name = "users"

urlpatterns = [
    path("", index, name="index"),
               path("signup/", register, name="signup"),
               path("blog/", blog, name="blog"),
               path("education/", education, name="education"),
            path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html')),
            path('verify/<slug:username>/', verify_code, name="verify"),  # ← new

]

