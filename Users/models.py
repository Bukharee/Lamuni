from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100)
    phone = models.TextField(max_length=20, blank=False, unique=True)
    is_verified = models.BooleanField(default=False)
    is_number_verified = models.BooleanField(default=False)
    reset_code = models.CharField(max_length=8, help_text='Enter code')