from django.shortcuts import get_object_or_404
from django import forms
from django.forms import ModelForm

from Loans.models import Loan, Sector, Record, SalesRecord, Requirement


class CreateLoanForm(ModelForm):
    sectors = forms.ModelMultipleChoiceField(
        queryset=Sector.objects.all(),
        widget=forms.CheckboxSelectMultiple

    )
    requirements = forms.ModelMultipleChoiceField(
        queryset=Requirement.objects.all(),
        widget=forms.CheckboxSelectMultiple

    )

    class Meta:
        model = Loan
        fields = ["program_title", "size", "sectors", "amount", "amount",
                  "paying_days", "grace_period",
                  "collateral", "requirements"]


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


class ApplyLoanForm(forms.Form):
    def __init__(self, user, loan_id, *args, **kwargs):
        print("the_uuser", user)
        print("loan_id", loan_id)
        super(ApplyLoanForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'address'
        self.fields['bvn'].widget.attrs['bvn'] = 'form-input'
        self.fields['nin'].widget.attrs['nin'] = 'form-input'
        self.fields['business_certificate'].widget.attrs['business_certificate'] = 'form-input'
        self.fields['financial_record'].widget.attrs['financial_record'] = 'form-input'
        self.fields['number_of_employee'].widget.attrs['number_of_employee'] = 'form-input'

        loan = get_object_or_404(Loan, id=int(loan_id))
        counter = 0
        # print(loan.requirements.all())
        for requirement in loan.requirements.all():
            print(getattr(user, requirement.requirement), requirement.requirement)
            if getattr(user, requirement.requirement):
                del self.fields[requirement.requirement]
                # print(self.fields)
                counter += 1
        copy_fields = self.fields.copy().keys()
        for key in copy_fields:
            if key not in [n.requirement for n in loan.requirements.all()]:
                del self.fields[key]
        print("nazo nan")
        if counter >= 7:
            print('none')
            return None

    address = forms.CharField(max_length=11)
    bvn = forms.IntegerField(help_text="input your bvn")
    nin = forms.CharField(max_length=11)
    business_certificate = forms.FileField()
    financial_record = forms.FileField()
    time_in_business = forms.IntegerField()
    number_of_employee = forms.IntegerField()
