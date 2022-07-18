from django.shortcuts import render
from .models import Lesson
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView


# Create your views here.

def lessons_list(request):

    context = {"lessons": Lesson.objects.all().order_by("date_published")}

    return render(request, "lessons-list.html", context)


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'lesson-detail.html', {'lesson': lesson})
