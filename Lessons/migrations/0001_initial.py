# Generated by Django 4.0.6 on 2022-07-28 20:03

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('finished', models.ManyToManyField(blank=True, related_name='finishers', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=30)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lessons.lesson')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('correct', models.ManyToManyField(blank=True, related_name='right', to='Lessons.quiz')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lessons.lesson')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wrong', models.ManyToManyField(blank=True, related_name='wrong', to='Lessons.quiz')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ScoreTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('feedback', models.TextField(max_length=400)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='Lessons.score')),
            ],
            options={
                'verbose_name': 'score Translation',
                'db_table': 'Lessons_score_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QuizTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('question', models.CharField(max_length=300)),
                ('option_a', models.CharField(max_length=300)),
                ('option_b', models.CharField(max_length=300)),
                ('option_c', models.CharField(max_length=300)),
                ('option_d', models.CharField(max_length=300)),
                ('suggestion', ckeditor.fields.RichTextField(help_text='Suggested reading when user fails the question.', verbose_name='Suggestion')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='Lessons.quiz')),
            ],
            options={
                'verbose_name': 'quiz Translation',
                'db_table': 'Lessons_quiz_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LessonTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=100)),
                ('desc', models.TextField(max_length=400)),
                ('blog', ckeditor.fields.RichTextField(help_text='Edit and enter text just like MS Word.', verbose_name='Blog')),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio/%Y/%m/%d/')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='Lessons.lesson')),
            ],
            options={
                'verbose_name': 'lesson Translation',
                'db_table': 'Lessons_lesson_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
