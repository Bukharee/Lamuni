from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth import get_user_model
from djmoney.money import Money

OWNER_TYPE = (('FSP', 'FSP'),
              ('User', 'User'))


# Create your models here.
class Wallet(models.Model):
    owner = models.OneToOneField(get_user_model(), related_name='wallet', on_delete=models.CASCADE)
    owner_type = models.CharField(choices=OWNER_TYPE, max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    balance = MoneyField(max_digits=14, decimal_places=2, default=Money(0, 'NGN'), default_currency='NGN')
