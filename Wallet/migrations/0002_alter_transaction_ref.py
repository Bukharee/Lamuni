# Generated by Django 4.0.6 on 2022-07-25 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='ref',
            field=models.CharField(max_length=400),
        ),
    ]
