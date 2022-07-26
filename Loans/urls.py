from django.urls import path
from .views import add_record, add_sales_record, fs, fr, GeneratePdf

app_name = 'Loans'

urlpatterns = [
    path('add/record/', add_record, name='add-record'),
    path('fs/', fs),
    path('fr/<int:pk>/', fr),
    path('add/sales/record/', add_sales_record, name='add-sales-record'),
    path('pdf/', GeneratePdf.as_view()),
]
