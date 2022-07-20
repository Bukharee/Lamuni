from django.urls import path
from .views import index, register,verify_code, send_reset_code
from django.contrib.auth import views as auth_views


app_name = "users"

urlpatterns = [
    path("", index, name="index"),
               path("signup/", register, name="signup"),
            path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html')),
            path('verify/<slug:username>/', verify_code, name="verify"),  # ← new
            path('password_reset/', send_reset_code, name="reset_password")
]

