from django.shortcuts import render
from .models import Lesson
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.

@login_required
def lessons_list(request):
    lesson = Lesson.objects.all()
    return render(request, 'lessons-list.html', {'lesson': lesson})


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'lesson-detail.html', {'lesson': lesson})
