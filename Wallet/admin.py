from django.contrib import admin
from .models import Wallet, Transaction


# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    list_display = ['owner', 'owner_type', 'balance']
    list_filter = ['date_created']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'amount', 'sender', 'receiver', 'date_created']
    list_filter = ['transaction_type', 'amount', 'date_created']


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
