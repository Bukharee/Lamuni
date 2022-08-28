from ast import Mod
from dataclasses import field
from django import forms
from django.forms import ModelForm

from Loans.models import Loan, Sector, Record, SalesRecord


class CreateLoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ["program_title", "size", "sectors", "amount", "amount",
                  "paying_days", "grace_period",
                  "collateral"]


class AddRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['amount', 'category']

    def __init__(self, *args, **kwargs):
        super(AddRecordForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['class'] = 'form-input'
        self.fields['category'].widget.attrs['class'] = 'form-input'

    def clean_amount(self):
        if self.cleaned_data['amount'] <= 0:
            self.add_error('amount', 'The field "Amount" should be greater than 0.')
        else:
            return self.cleaned_data['amount']


class AddSalesRecordForm(ModelForm):
    class Meta:
        model = SalesRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddSalesRecordForm, self).__init__(*args, **kwargs)
        self.fields["item_name"].widget.attrs['class'] = 'form-input'
        self.fields["quantity"].widget.attrs['class'] = 'form-input'
        self.fields["cost_price_per_item"].widget.attrs['class'] = 'form-input'
        self.fields["selling_price_per_item"].widget.attrs['class'] = 'form-input'

    def clean_amount(self):
        if self.cleaned_data['cost_price_per_item'] <= 0:
            self.add_error('cost_price_per_item', 'The field "Cost Price" should be greater than 0.')
        else:
            return self.cleaned_data['cost_price_per_item']

        if self.cleaned_data['selling_price_per_item'] <= 0:
            self.add_error('selling_price_per_item', 'The field "Selling Price" should be greater than 0.')
        else:
            return self.cleaned_data['selling_price_per_item']
    #     model = Loan
    #     fields = ["program_title", "size", "sectors", "amount", "amount",
    #               "paying_days", "grace_period",
    #               "collateral"]
    #
    # sectors = forms.ModelMultipleChoiceField(
    #     queryset=Sector.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    #
    # )
