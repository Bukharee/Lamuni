from django.contrib import admin
from .models import Loan, Beneficiaries

# Register your models here.
admin.site.register(Loan)
admin.site.register(Beneficiaries)
