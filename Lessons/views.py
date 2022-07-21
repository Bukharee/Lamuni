from django.shortcuts import render
from .models import Lesson, Quiz, Score
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.
def lessons_list(request):
    context = {"lessons": Lesson.objects.all().order_by("date_published")}

    return render(request, "lessons-list.html", context)


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'lesson-detail.html', {'lesson': lesson})


@login_required
def mark_lesson_completed(request, pk):
    user = request.user
    lesson = get_object_or_404(Lesson, pk=pk)

    if user not in lesson.finished.all():
        lesson.finished.add(user)
        lesson.save()

    return render(request, 'lesson-detail.html', {'lesson': lesson})


@login_required
def quiz(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        print(request.POST)
        questions = Quiz.objects.filter(lesson=lesson)
        total = 0
        wrong = 0
        correct = 0
        score = Score.objects.create(lesson=lesson, user=request.user)
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.answer)
            if q.answer == request.POST.get(q.question):
                score.correct.add(q)
                score.save()
                correct += 1
            else:
                score.wrong.add(q)
                score.save()
                wrong += 1
            score.total = total
            score.save()

        percent = (correct / total) * 100
        context = {
            'score': score,
            'correct': score.correct,
            'wrong': score.wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'quiz-result.html', context)

    else:
        questions = Quiz.objects.filter(lesson=lesson)
        context = {
            'questions': questions
        }
        return render(request, 'quiz.html', context)
