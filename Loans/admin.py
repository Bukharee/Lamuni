from django.contrib import admin
from .models import Record, FinancialRecord, SalesRecord

# Register your models here.
admin.site.register(Record)
admin.site.register(FinancialRecord)
admin.site.register(SalesRecord)
