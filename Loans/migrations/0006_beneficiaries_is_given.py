# Generated by Django 4.0.6 on 2022-07-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loans', '0005_remove_beneficiaries_is_given'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiaries',
            name='is_given',
            field=models.BooleanField(default=False),
        ),
    ]
