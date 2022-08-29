from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField




class Sector(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.name)

# Create your models here.
TIME_IN_BUSINESS_CHOICES = (('Less than 1 year', 'Less than 1 year'),
                            ('2 years', '2 years'),
                            ('3 years', '3 years'),
                            ('4 years', '4 years'),
                            ('5 years', '5 years'),
                            ('Above 5 years', 'Above 5 years'),)
BUSINESS_SIZE = (('MICRO', 'MICRO'), ('SMALL', 'SMALL'), ('MEDIUM', 'MEDIUM'),)

class User(AbstractUser):
    name = models.CharField(max_length=100)
    phone = models.TextField(max_length=20, blank=False, unique=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_number_verified = models.BooleanField(default=False)
    reset_code = models.CharField(max_length=8, help_text='Enter code')
    is_kyc_verified = models.BooleanField(default=False)
    address = models.CharField(max_length=200, blank=False, null=True)
    bvn = models.PositiveIntegerField(blank=False, null=True, max_length=11)
    nin = models.PositiveIntegerField(blank=False, null=True, max_length=11)
    business_certificate = models.FileField(upload_to='business_certificate/%Y/%m/', null=True, blank=True)
    financial_record = models.FileField(upload_to='financial_record/%Y/%m/', null=True, blank=True)
    time_in_business = models.CharField(max_length=30, choices=TIME_IN_BUSINESS_CHOICES, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.DO_NOTHING, blank=True, null=True)
    size = models.CharField(choices=BUSINESS_SIZE, max_length=20)
    number_of_employee = models.PositiveIntegerField(blank=True, null=True)




    def validate_bvn(request):
        """this will be used to validate uses bvn"""
        pass
