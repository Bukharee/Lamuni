from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Lesson


# Register your models here.

@admin.register(Lesson)
class LessonAdmin(TranslatableAdmin):
    search_fields = ['translations__title', 'translations__desc', ]
