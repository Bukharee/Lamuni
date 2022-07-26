from django.urls import path
from .views import add_record

app_name = 'Loans'

urlpatterns = [
    path('add/record/', add_record, name='add-record'),
]
