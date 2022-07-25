from datetime import timezone

from django.core.exceptions import ValidationError
from django.db import models
from djmoney.models.fields import MoneyField
from Users.models import User
from djmoney.money import Money
from django.shortcuts import get_object_or_404

OWNER_TYPE = (('FSP', 'FSP'),
              ('User', 'User'))

TRANSACTION_TYPE = (('Credit', 'Credit'), ('Debit', 'Debit'))


# Create your models here.
class Wallet(models.Model):
    owner = models.OneToOneField(User, related_name='wallet', on_delete=models.CASCADE, unique=True)
    owner_type = models.CharField(choices=OWNER_TYPE, max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    balance = MoneyField(max_digits=14, decimal_places=2, default=Money(0, 'NGN'), default_currency='NGN')

    @classmethod
    def recharge_wallet(cls, amount, receiver, description):

        receiver_wallet = get_object_or_404(Wallet, owner=receiver)
        receiver_wallet.balance += amount
        receiver_wallet.save()

        recharge_transaction = Transaction.objects.create(
            amount=amount,
            receiver_wallet=receiver,
            transaction_type="Credit",
            date_created=timezone.now,
            description=description,

        )

        return recharge_transaction

    @classmethod
    def withdraw_wallet(cls, amount, description, wallet_to_withdraw):

        if amount > wallet_to_withdraw.balance:
            raise ValidationError("Insufficient account balance, please try amount less than your balance")

        wallet_to_withdraw.balance -= amount
        wallet_to_withdraw.save()

        recharge_transaction = Transaction.objects.create(
            amount=amount,
            transaction_type="Debit",
            date_created=timezone.now,
            description=description,

        )

        return recharge_transaction

    @classmethod
    def transfer_money(cls, amount, sender, receiver, description):

        sender_wallet = get_object_or_404(Wallet, owner=sender)
        sender_wallet -= amount

        transfer_transaction = Transaction.objects.create(
            amount=amount,
            sender=sender,
            receiver=receiver,
            transaction_type="Debit",
            date_created=timezone.now,
            description=description,
        )

        receiver_wallet = get_object_or_404(Wallet, owner=receiver)
        receiver_wallet.balance += amount
        transfer_transaction = Transaction.objects.create(
            amount=amount,
            sender=sender,
            receiver=receiver,
            transaction_type="Credit",
            date_created=timezone.now,
            description=description,
        )

        sender_wallet.save()
        receiver_wallet.save()
        return transfer_transaction


class Transaction(models.Model):
    transaction_type = models.CharField(max_length=45, choices=TRANSACTION_TYPE, default='',
                                        verbose_name='Transaction Type')
    amount = MoneyField(max_digits=14, decimal_places=2, default=Money(0, 'NGN'), default_currency='NGN',
                        verbose_name='Amount')
    description = models.CharField(max_length=250, default='', help_text='write your description here',
                                   verbose_name='Description', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender',
                               verbose_name='Sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver',
                                 verbose_name='Receiver')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Transaction Date')
    ref = models.CharField(max_length=400, unique=True)
