# Generated by Django 4.0.6 on 2022-08-28 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_user_number_of_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
