from django.urls import path
from .views import index, register,verify_code, send_reset_code, reset_verify, reset_password, education, lesson_detail, lesson_done, quiz, quiz_result
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("", index, name="index"),
    path("education/", education, name="education"),
    path("lesson-detail/", lesson_detail, name="lesson-detail"),
    path("lesson-done/", lesson_done, name="lesson-done"),
    path("quiz/", quiz, name="quiz"),
    path("quiz-result/", quiz_result, name="quiz-result"),
    path("signup/", register, name="signup"),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html')),
    path('verify/<slug:username>/', verify_code, name="verify"),  # ← new
    path('send_reset/', send_reset_code, name="reset_code"),
    path('reset_verify/<slug:username>/', reset_verify, name="reset_verify"),
    path('password_reset/<slug:username>/<int:code>/', reset_password, name="reset_password"),
]

