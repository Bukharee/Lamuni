from django.contrib import admin
from .models import Loan, Record, FinancialRecord, SalesRecord, Beneficiaries, Requirement

# Register your models here.
admin.site.register(Loan)
admin.site.register(Record)
admin.site.register(FinancialRecord)
admin.site.register(SalesRecord)
admin.site.register(Beneficiaries)
admin.site.register(Requirement)