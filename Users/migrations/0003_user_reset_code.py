# Generated by Django 4.0.6 on 2022-07-19 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_code',
            field=models.CharField(default=0, help_text='Enter code', max_length=8),
            preserve_default=False,
        ),
    ]
