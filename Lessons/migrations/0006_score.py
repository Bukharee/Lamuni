# Generated by Django 4.0.6 on 2022-07-20 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Lessons', '0005_quiz_quiztranslation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('correct', models.ManyToManyField(blank=True, null=True, related_name='right', to='Lessons.quiz')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lessons.lesson')),
                ('wrong', models.ManyToManyField(blank=True, null=True, related_name='wrong', to='Lessons.quiz')),
            ],
        ),
    ]
