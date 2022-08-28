from django.shortcuts import get_object_or_404
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
        model = Loan
        fields = ["program_title", "size", "sectors", "amount", "amount",
                  "paying_days", "grace_period",
                  "collateral"]

    sectors = forms.ModelMultipleChoiceField(
        queryset=Sector.objects.all(),
        widget=forms.CheckboxSelectMultiple

    )

class ApplyLoanForm(forms.Form):
    def __init__(self, user, loan_id, *args, **kwargs):
        print("the_uuser", user)
        print("loan_id", loan_id)
        super(ApplyLoanForm, self).__init__(*args, **kwargs)
        loan = get_object_or_404(Loan, id=int(loan_id))
        counter = 0
        # print(loan.requirements.all())
        for requirement in loan.requirements.all():
                print(getattr(user, requirement.requiremenent), requirement.requiremenent)
                if getattr(user, requirement.requiremenent):
                    del self.fields[requirement.requiremenent]
                    # print(self.fields)
                    counter += 1
        copy_fields = self.fields.copy().keys()
        for key in copy_fields:
            if key not in [n.requiremenent for n in loan.requirements.all()]:
                del self.fields[key]
        print("nazo nan")
        if counter >= 7:
            print('none')
            return None

    address = forms.CharField(max_length=11)
    bvn = forms.IntegerField(help_text="input your bvn")
    nin =  forms.CharField(max_length=11)
    business_certificate = forms.FileField()
    financial_record = forms.FileField()
    time_in_business = forms.IntegerField()
    number_of_employee = forms.IntegerField()
