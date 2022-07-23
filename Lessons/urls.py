from django.urls import path
from .views import lesson_detail, lessons_list, mark_lesson_completed, quiz

app_name = 'Lessons'

urlpatterns = [
    path('lessons/list/', lessons_list, name='lessons'),
    path('lesson/detail/<int:pk>/', lesson_detail, name='detail'),
    path('mark/completed/<int:pk>/', mark_lesson_completed, name='completed'),
    path('quiz/<int:pk>/', quiz, name='quiz'),
]
