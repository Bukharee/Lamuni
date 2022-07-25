from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Wallet


# Create your views here.
def view_wallet(request):

    user = request.user

    wallet = get_object_or_404(Wallet, owner=user)

    context = {
        'wallet': wallet,
    }
    return render(request, 'wallet.html', context)
