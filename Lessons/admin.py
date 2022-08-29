from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Lesson, Quiz, Score


# Register your models here.

@admin.register(Lesson)
class LessonAdmin(TranslatableAdmin):
    search_fields = ['translations__title', 'translations__desc', ]

@admin.register(Quiz)
class QuizAdmin(TranslatableAdmin):
    list_display = ['question', ]


@admin.register(Score)
class ScoreAdmin(TranslatableAdmin):
    list_display = ['user', ]
    fields = ["title", "desc", "blog", "audio"]