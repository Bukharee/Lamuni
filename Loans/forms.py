from ast import Mod
from dataclasses import field
from django import forms
from django.forms import ModelForm

from Loans.models import Loan, Sector


class CreateLoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ["program_title", "size", "sectors", "amount", "amount", 
        "paying_days", "grace_period",
        "collateral"]

    sectors = forms.ModelMultipleChoiceField(
            queryset=Sector.objects.all(),
            widget=forms.CheckboxSelectMultiple

        )
