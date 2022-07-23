from django.urls import path
from .views import index, singup, login, education, lesson_detail, lesson_done, quiz, quiz_result

app_name = "users"

urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),
    path("signup/", singup, name="signup"),
    path("education/", education, name="education"),
    path("lesson-detail/", lesson_detail, name="lesson-detail"),
    path("lesson-done/", lesson_done, name="lesson-done"),
    path("quiz/", quiz, name="quiz"),
    path("quiz-result/", quiz_result, name="quiz-result"),
]

