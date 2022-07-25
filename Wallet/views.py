import random
import string
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import FilterTransactionsForm, RechargeWallet, WithdrawWallet, TransferMoney
from .models import Wallet


# Create your views here.
def view_wallet(request):
    user = request.user

    wallet = get_object_or_404(Wallet, owner=user)

    context = {
        'wallet': wallet,
    }
    return render(request, 'wallet.html', context)


def recharge(request,  *args, **kwargs):
    if request.method == "POST":
        recharge_form = RechargeWallet(request.POST)
        if recharge_form.is_valid():
            owner_id = request.user.wallet.id
            direct = request.user.wallet.slug
            amount = recharge_form.cleaned_data['amount']
            description = recharge_form.cleaned_data['description']
            wallet = get_object_or_404(Wallet, id=owner_id)
            ref_code = wallet_ref_code_generator()
            # payment = pay_with_pay_stack(request, amount, ref_code)
            if payment:
                recharge_transaction = Wallet.recharge_wallet(amount, wallet, description)
            return HttpResponseRedirect('/wallet/' + direct)

    else:
        recharge_form = RechargeWallet()

    context = {
        'recharge_form': recharge_form
    }
    return render(request, 'wallets/recharge_form.html', context)


def withdraw(request,  *args, **kwargs):
    if request.method == "POST":
        withdraw_form = WithdrawWallet(request.POST)
        if withdraw_form.is_valid():
            owner_id = request.user.wallet.id
            direct = request.user.wallet.slug
            amount = withdraw_form.cleaned_data['amount']
            description = withdraw_form.cleaned_data['description']
            wallet_to_withdraw = get_object_or_404(Wallet, id=owner_id)
            withdraw_transaction = Wallet.withdraw_wallet(amount, description, wallet_to_withdraw)
            return HttpResponseRedirect('/wallet/' + direct)

    else:
        withdraw_form = WithdrawWallet()

    context = {
        "withdraw_form": withdraw_form
    }
    return render(request, 'wallets/withdraw_form.html', context)


def transfer(request, *args, **kwargs):
    if request.method == "POST":
        transfer_form = TransferMoney(request.POST)
        owner_id = request.user.wallet.id
        sender_wallet = request.user.wallet
        direct = request.user.wallet.slug
        if transfer_form.is_valid():
            amount = transfer_form.cleaned_data['amount']
            description = transfer_form.cleaned_data['description']
            receiver = transfer_form.cleaned_data['receiver_wallet']
            receiver_id = receiver.id
            wallet_to_transfer = get_object_or_404(Wallet, id=receiver_id)
            transfer_transaction = Wallet.transfer_money(amount, sender_wallet, receiver, description)
            return HttpResponseRedirect('/wallet/' + direct)

    else:
        transfer_form = TransferMoney()

    context = {
        "transfer_form": transfer_form,
    }
    return render(request, "wallets/transfer_form.html", context)

def wallet_ref_code_generator():
    guess = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    ref_code = 'WLT' + guess
    return ref_code
