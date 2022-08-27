from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import RechargeWallet, WithdrawWallet, TransferMoney
from .models import Wallet, wallet_ref_code_generator
from django.template import loader
from django.contrib.auth.decorators import login_required
import sys
import json
import requests


# Create your views here
@login_required
def view_wallet(request):
    user = request.user

    try:
        wallet = Wallet.objects.get(owner=user)

    except Exception:

        wallet = Wallet.objects.create(
            owner=user,
            owner_type="User", )
    headers = {
        "Authorization": "dskjdks",
        "Content-Type": "application/json",
        "sandbox-key": "iA2AJuzAxaPw8VE0PYMTAFbVUTKQ4WAN1661622415",
    }
    url = "https://fsi.ng/api/v1/flutterwave/v3/virtual-account-numbers"
    data = ({
        "email": user.email,
        "is_permanent": True,
        "bvn": user.bvn,
        "phonenumber": user.phone,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "narration": "Lamuni",
    })

    my_data = requests.request("POST", url, json=data, headers=headers)
    print(my_data)
    if my_data.status_code not in [200, 203]:
        print("There was an error retrieving the data from Linkshare: {}:{}".format(
            my_data.status_code, my_data.text
        )
        )

    data = (json.loads(my_data.text)["data"])

    print(data)
    wallet.account_number = data['account_number']
    wallet.account_name = data['note']
    wallet.bank = data['bank_name']

    wallet.save()

    template = loader.get_template('wallet_cabinet.html')

    # fill_up_wallet_form = RechargeWallet()
    # withdraw_money_form = WithdrawWallet()
    context = {
        'wallet': wallet,
        # 'fillUp_wallet_form': fill_up_wallet_form,
        # 'withdraw_money_form': withdraw_money_form
    }

    return HttpResponse(template.render(context, request))


def recharge(request, *args, **kwargs):
    if request.method == "POST":
        recharge_form = RechargeWallet(request.POST)
        if recharge_form.is_valid():
            owner = request.user
            amount = recharge_form.cleaned_data['amount']
            description = recharge_form.cleaned_data['description']
            ref_code = wallet_ref_code_generator()
            # payment = pay_with_pay_stack(request, amount, ref_code)
            recharge_transaction = Wallet.recharge_wallet(amount, owner, description)
            return HttpResponseRedirect('/wallet/')

    else:
        recharge_form = RechargeWallet()

    context = {
        'recharge_form': recharge_form
    }
    return render(request, 'recharge_form.html', context)


def withdraw(request, *args, **kwargs):
    if request.method == "POST":
        withdraw_form = WithdrawWallet(request.POST)
        if withdraw_form.is_valid():
            owner = request.user
            amount = withdraw_form.cleaned_data['amount']
            description = withdraw_form.cleaned_data['description']
            wallet_to_withdraw = get_object_or_404(Wallet, owner=owner)
            withdraw_transaction = Wallet.withdraw_wallet(amount, description, wallet_to_withdraw)
            return HttpResponseRedirect('/wallet/')

    else:
        withdraw_form = WithdrawWallet()

    context = {
        "withdraw_form": withdraw_form
    }
    return render(request, 'withdraw_form.html', context)


def transfer(request, *args, **kwargs):
    if request.method == "POST":
        transfer_form = TransferMoney(request.POST)
        sender = request.user
        if transfer_form.is_valid():
            amount = transfer_form.cleaned_data['amount']
            description = transfer_form.cleaned_data['description']
            receiver = transfer_form.cleaned_data['receiver']
            wallet_to_transfer = get_object_or_404(Wallet, owner=receiver)
            transfer_transaction = Wallet.transfer_money(amount, sender, receiver, description)
            return HttpResponseRedirect('/wallet/')

    else:
        transfer_form = TransferMoney()

    context = {
        "transfer_form": transfer_form,
    }
    return render(request, "transfer_form.html", context)
