<<<<<<< HEAD
# Generated by Django 4.0.6 on 2022-07-26 09:30
=======
# Generated by Django 4.0.6 on 2022-07-26 10:10
>>>>>>> main

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.TextField(max_length=20, null=True, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_number_verified', models.BooleanField(default=False)),
                ('reset_code', models.CharField(help_text='Enter code', max_length=8)),
                ('is_kyc_verified', models.BooleanField(default=False)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('address', models.TextField(blank=True, max_length=200, null=True)),
                ('bvn', models.PositiveIntegerField(blank=True, null=True)),
                ('nin', models.PositiveIntegerField(blank=True, null=True)),
                ('nin_file', models.FileField(blank=True, null=True, upload_to='nins/%Y/%m/')),
                ('business_certificate', models.FileField(blank=True, null=True, upload_to='business_certificate/%Y/%m/')),
                ('financial_record', models.FileField(blank=True, null=True, upload_to='financial_record/%Y/%m/')),
                ('time_in_business', models.CharField(blank=True, choices=[('Less than 1 year', 'Less than 1 year'), ('2 years', '2 years'), ('3 years', '3 years'), ('4 years', '4 years'), ('5 years', '5 years'), ('Above 5 years', 'Above 5 years')], max_length=30, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
