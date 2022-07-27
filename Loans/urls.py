from django.urls import path
from .views import create_loan, loan_details, dashboard

urlpatterns = [
    path('create-loan/', create_loan, name="create_loan"),
    path('loan-details/<int:pk>/', loan_details, name="loan_details"),
    path('dashboard/', dashboard, name="dashboard")
    ]