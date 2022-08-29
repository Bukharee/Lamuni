from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


# Create your models here.
class Lesson(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, blank=False, null=False),
        desc=models.TextField(max_length=400, blank=False, null=False),
        blog=RichTextField('Blog', help_text='Edit and enter text just like MS Word.'),
        audio=models.FileField(upload_to='audio/%Y/%m/%d/', null=True, blank=True),
    )
    finished = models.ManyToManyField(get_user_model(), related_name='finishers', blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('lessons:detail', args=[self.pk])

    def get_quiz_url(self):
        return reverse('lessons:quiz', args=[self.pk])


ANSWER_CHOICES = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),)


class Quiz(TranslatableModel):
    translations = TranslatedFields(
        question=models.CharField(max_length=300, blank=False, null=False),
        option_a=models.CharField(max_length=300, blank=False, null=False),
        option_b=models.CharField(max_length=300, blank=False, null=False),
        option_c=models.CharField(max_length=300, blank=False, null=False),
        option_d=models.CharField(max_length=300, blank=False, null=False),
        suggestion=RichTextField('Suggestion', help_text='Suggested reading when user fails the question.',
                                 blank=False, null=False),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    answer = models.CharField(max_length=30, choices=ANSWER_CHOICES)

    # def __str__(self):
    #     return self.lesson.id

    def get_absolute_url(self):
        return reverse('lessons:quiz', args=[self.pk])


class Score(TranslatableModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    wrong = models.ManyToManyField(Quiz, related_name='wrong', blank=True)
    correct = models.ManyToManyField(Quiz, related_name='right', blank=True)
    total = models.PositiveIntegerField(default=0)
    translations = TranslatedFields(
        feedback=models.TextField(max_length=400, blank=False, null=False),
    )

    # def __str__(self):
    #     return self.lesson.id
