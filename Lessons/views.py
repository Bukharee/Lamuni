from django.shortcuts import render
from .models import Lesson, Quiz, Score
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.
def lessons_list(request):
    context = {"lessons": Lesson.objects.all().order_by("date_published")}
    return render(request, "lessons/lessons-list.html", context)


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'lessons/lesson-detail.html', {'lesson': lesson})


@login_required
def mark_lesson_completed(request, pk):
    user = request.user
    lesson = get_object_or_404(Lesson, pk=pk)

    if user not in lesson.finished.all():
        lesson.finished.add(user)
        lesson.save()

    return render(request, 'lessons/lesson-done.html', {'lesson': lesson})


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
        wrong_q = []
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
                wrong_q.append(q)
            score.total = total
            score.save()
        try: 
            percent = (correct / total) * 100
        except ZeroDivisionError:
            percent = 0
        context = {
            'score': score,
            'correct': score.correct,
            'wrong': score.wrong,
            'wrong_qs': wrong_q,
            'percent': percent,
            'total': total
        }
        return render(request, 'lessons/quiz-result.html', context)

    else:
        questions = Quiz.objects.filter(lesson=lesson)
        context = {
            'questions': questions
        }
        print(questions)
        return render(request, 'lessons/quiz.html', context)


@login_required
def quiz_list(request):
    context = {"lessons": Lesson.objects.all().order_by("date_published")}
    return render(request, 'lessons/quiz_list.html', context)
