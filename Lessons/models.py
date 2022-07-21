from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model


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

    # def __str__(self):
    #     return self.id


ANSWER_CHOICES = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),)


class Quiz(TranslatableModel):
    translations = TranslatedFields(
        question=models.CharField(max_length=300, blank=False, null=False),
        option_a=models.CharField(max_length=300, blank=False, null=False),
        option_b=models.CharField(max_length=300, blank=False, null=False),
        option_c=models.CharField(max_length=300, blank=False, null=False),
        option_d=models.CharField(max_length=300, blank=False, null=False),
        suggestion=RichTextField('Blog', help_text='Suggested reading when user fails the question.',
                                 blank=False, null=False),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    answer = models.CharField(max_length=30, choices=ANSWER_CHOICES)

    # def __str__(self):
    #     return self.lesson.id


class Score(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    wrong = models.ManyToManyField(Quiz, related_name='wrong', blank=True)
    correct = models.ManyToManyField(Quiz, related_name='right', blank=True)
    total = models.PositiveIntegerField(default=0)

    # def __str__(self):
    #     return self.lesson.id
