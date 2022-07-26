from django.urls import path
from .views import add_record, add_sales_record

app_name = 'Loans'

urlpatterns = [
    path('add/record/', add_record, name='add-record'),
    path('add/sales/record/', add_sales_record, name='add-sales-record'),
]
