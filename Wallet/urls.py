from django.urls import path
from .views import view_wallet, recharge, withdraw, transfer

app_name = 'Lessons'

urlpatterns = [
    path('wallet/', view_wallet, name='index'),
    path('wallet/recharge/', recharge, name='recharge'),
    path('wallet/withdraw/', withdraw, name='withdraw'),
    path('wallet/transfer/', transfer, name='transfer')
]
