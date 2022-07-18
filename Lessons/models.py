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
        audio=models.FileField(),
    )
    finished = models.ManyToManyField(get_user_model(), related_name='finishers', blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
