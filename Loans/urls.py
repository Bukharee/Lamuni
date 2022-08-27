from django.urls import path
from .views import create_loan, loan_details, dashboard, loans_list, fsp_profile, \
    loan_beneficiaries, add_record, add_sales_record, fs, fr, GeneratePdf, user_loan_details

app_name = 'loans'

urlpatterns = [
    path('add/record/', add_record, name='add-record'),
    path('fs/', fs),
    path('fr/<int:pk>/', fr),
    path('add/sales/record/', add_sales_record, name='add-sales-record'),
    path('pdf/', GeneratePdf.as_view()),
    path('create-loan/', create_loan, name="create_loan"),
    path('loan-details/<int:pk>/', loan_details, name="loan_details"),
    path('user-loan-details/<int:pk>/', user_loan_details, name="user-loan-details"),
    path('dashboard/', dashboard, name="dashboard"),
    path('loans/', loans_list, name='loans_list'),
    path('fsp/profile/', fsp_profile, name='profile'),
    path('loans/<int:pk>/beneficiaries/', loan_beneficiaries, name='beneficiaries'),
]
