from django.urls import path
from .views import create_loan, loan_details, dashboard, add_record, add_sales_record, fs, fr, GeneratePdf

app_name = 'Loans'

urlpatterns = [
    path('add/record/', add_record, name='add-record'),
    path('fs/', fs),
    path('fr/<int:pk>/', fr),
    path('add/sales/record/', add_sales_record, name='add-sales-record'),
    path('pdf/', GeneratePdf.as_view()),
    path('create-loan/', create_loan, name="create_loan"),
    path('loan-details/<int:pk>/', loan_details, name="loan_details"),
    path('dashboard/', dashboard, name="dashboard")
]