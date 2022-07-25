from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField

# Create your models here.
BUSSINESS_SIZE = (('MICRO', 'MICRO'),('SMALL', 'SMALL'),('MEDIUM', 'MEDIUM'),)


class Sector(models.Model):
    name = models.CharField(max_length=200)

class FSP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)

class Beneficiaries(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    time_applied = models.DateTimeField()
    time_payed = models.DateField()
    is_payed = models.DateTimeField()
    time_to_pay = models.DateTimeField() #oficailly the time the loan suppose to be paid

    
class Loan(models.Model):
    fsp = models.ForeignKey(FSP, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    program_title = models.CharField(max_length=200)
    size = MultiSelectField(choices=BUSSINESS_SIZE, max_choices=3, max_length=100)
    sectors = models.ManyToManyField(Sector)
    amount = models.PositiveIntegerField()
    beneficiaries = models.ManyToManyField(get_user_model())
    is_active = models.BooleanField(default=False)
    number_of_employee = models.PositiveIntegerField()
    amount = models.PositiveBigIntegerField()
    paying_days = models.PositiveIntegerField()
    grace_period = models.PositiveIntegerField()
    collateral = models.CharField(max_length=200, blank=True, null=True)
