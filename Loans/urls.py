from django.urls import path
from .views import (create_loan, loan_details, dashboard, loans_list, fsp_profile,
 loan_beneficiaries, add_record, add_sales_record, fs, fr, GeneratePdf, list_loans, 
 apply_loan, users_credentials, grant_loan, deny_loan, recommended_loans)

app_name = 'loans'

urlpatterns = [
    path('add/record/', add_record, name='add-record'),
    path('fs/', fs),
    path('fr/<int:pk>/', fr),
    path('add/sales/record/', add_sales_record, name='add-sales-record'),
    path('pdf/', GeneratePdf.as_view()),
    path('create-loan/', create_loan, name="create_loan"),
    path('loan-details/<int:pk>/', loan_details, name="loan_details"),
    path('dashboard/', dashboard, name="dashboard"),
    path('loans/', loans_list, name='loans_list'),
    path('profile/', fsp_profile, name='profile'),
    path('loans/<int:pk>/beneficiaries/', loan_beneficiaries, name='beneficiaries'),
    path('list-loans', list_loans, name="list_loans"),
    path('apply-loan/<int:id>/', apply_loan, name="apply_loan"),
    path('users-credential/<int:loan_id>/<slug:username>/', users_credentials, name="users_loan_requirements"),
    path('grant-loan/<int:loan_id>/<slug:username>/', grant_loan, name="approve_loan"),
    path('deny-loan/<int:loan_id>/<slug:username>/', deny_loan, name="deny_loan"),
    path("recommended-loans/", recommended_loans, name="recommended_loans")
]
