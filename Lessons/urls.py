from django.urls import path
from .views import lesson_detail, lessons_list

app_name = 'Lessons'

urlpatterns = [
    path('lessons/list/', lessons_list, name='lessons'),
    path('lesson/detail/<int:pk>/', lesson_detail, name='detail'),
]
