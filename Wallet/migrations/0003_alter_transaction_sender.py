# Generated by Django 4.0.6 on 2022-07-25 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Wallet', '0002_alter_transaction_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
    ]