from dataclasses import field
from django.forms import forms, ModelForm
from .models import Record, SalesRecord


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
        if self.cleaned_data['amount'] <= 0:
            self.add_error('amount', 'The field "Amount" should be greater than 0.')
        else:
            return self.cleaned_data['amount']


class AddSalesRecordForm(ModelForm):
    class Meta:
        model = SalesRecord
        fields = '__all__'

    def clean_amount(self):
        if self.cleaned_data['cost_price_per_item'] <= 0:
            self.add_error('cost_price_per_item', 'The field "Cost Price" should be greater than 0.')
        else:
            return self.cleaned_data['cost_price_per_item']

        if self.cleaned_data['selling_price_per_item'] <= 0:
            self.add_error('selling_price_per_item', 'The field "Selling Price" should be greater than 0.')
        else:
            return self.cleaned_data['selling_price_per_item']
