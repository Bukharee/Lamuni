# Generated by Django 4.0.6 on 2022-08-27 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
