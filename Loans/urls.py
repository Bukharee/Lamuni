from django.urls import path
from .views import create_loan, loan_details, dashboard, loans_list, fsp_profile

app_name = 'loans'

urlpatterns = [
    path('create-loan/', create_loan, name="create_loan"),
    path('loan-details/<int:pk>/', loan_details, name="loan_details"),
    path('dashboard/', dashboard, name="dashboard"),
    path('loans/', loans_list, name='loans_list'),
    path('profile/', fsp_profile, name='profile')
]
