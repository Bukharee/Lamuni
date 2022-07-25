from django.contrib import admin
from .models import Wallet


# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    list_display = ['owner', 'owner_type', 'balance']
    list_filter = ['date_created']


admin.site.register(Wallet, WalletAdmin)
