from django.urls import path
from .views import lesson_detail, lessons_list, mark_lesson_completed, quiz, quiz_list, lesson_done

app_name = 'lessons'

urlpatterns = [
    path('lessons/list/', lessons_list, name='lessons'),
    path('lesson/detail/<int:pk>/', lesson_detail, name='detail'),
    path('mark/completed/<int:pk>/', mark_lesson_completed, name='completed'),
    path('quiz/list/', quiz_list, name='quiz-list' ),
    path('quiz/<int:pk>/', quiz, name='quiz'),
    path('lesson/lesson-done/<int:pk>/', lesson_done, name='lesson-done')
]
