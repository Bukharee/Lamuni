# Generated by Django 4.0.6 on 2022-07-18 16:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Lessons', '0002_auto_20220717_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='finished',
        ),
        migrations.AddField(
            model_name='lesson',
            name='finished',
            field=models.ManyToManyField(blank=True, related_name='finishers', to=settings.AUTH_USER_MODEL),
        ),
    ]