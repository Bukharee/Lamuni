from django.urls import path
from .views import lessons_list, lesson_detail

app_name = 'Lessons'

urlpatterns = [
    path('lessons/', lessons_list, name='lessons'),
    path('lesson/detail/<int:pk>/', lesson_detail, name='detail'),
]
