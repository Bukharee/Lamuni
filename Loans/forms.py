from dataclasses import field
from django.forms import forms, ModelForm
from .models import Record


class CreateLoanForm(forms.Form):
    class Meta:
        fields = ["program_title", "size", "sectors", "amount", "amount",
                  "paying_days", "grace_period",
                  "collateral"]


class AddRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['amount', 'category']

    def clean_amount(self):
        if self.cleaned_data['amount'] < 0:
            self.add_error('amount', 'The field "Amount" should not greater than 0.')
        else:
            return self.cleaned_data['amount']
