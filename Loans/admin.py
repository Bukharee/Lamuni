from django.contrib import admin
from .models import Loan, Record, FinancialRecord, SalesRecord, Beneficiaries, Requirement, Assets, Liability,\
    BalanceSheet, Payment


# Register your models here.
admin.site.register(Loan)
admin.site.register(Record)
admin.site.register(FinancialRecord)
admin.site.register(SalesRecord)
admin.site.register(Beneficiaries)
admin.site.register(Requirement)
admin.site.register(Assets)
admin.site.register(Liability)
admin.site.register(BalanceSheet)
admin.site.register(Payment)

