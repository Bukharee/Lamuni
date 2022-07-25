from django.urls import path
from .views import view_wallet

app_name = 'Lessons'

urlpatterns = [
    path('wallet/', view_wallet, name='wallet'),
]
