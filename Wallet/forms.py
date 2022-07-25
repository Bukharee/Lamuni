from django import forms
from .models import Transaction


class RechargeWallet(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']

    def clean_amount(self):
        if self.cleaned_data['amount'] == 0:
            self.add_error('amount', 'The field "Amount" should not be greater than 0.')
        else:
            return self.cleaned_data['amount']


class WithdrawWallet(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']

    def clean_amount(self):
        if self.cleaned_data['amount'] == 0:
            self.add_error('amount', 'The field "Amount" should not be greater than 0.')
        else:
            return self.cleaned_data['amount']


class TransferMoney(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'receiver_wallet', 'description']

    def clean_amount(self):
        if self.cleaned_data['amount'] == 0:
            self.add_error('amount', 'The field "Amount" should not be greater than 0.')
        else:
            return self.cleaned_data['amount']


class FilterTransactionsForm(forms.Form):
    wallet_id = forms.CharField(label='Wallet id', max_length=100)
    start_date = forms.DateTimeField(label="Date from", required=False)
    fin_date = forms.DateTimeField(label="Date until", required=False)
    as_csv = forms.BooleanField(label="Load as CSV file", required=False)
