# Generated by Django 4.0.6 on 2022-07-25 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Loans', '0003_remove_loan_number_of_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiaries',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='beneficiary', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loan',
            name='fsp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fsp', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FSP',
        ),
    ]