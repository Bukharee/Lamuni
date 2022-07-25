from dataclasses import field
from django.forms import forms


class CreateLoanForm(forms.Form):
    class Meta:
        fields = ["program_title", "size", "sectors", "amount", "amount", 
        "paying_days", "grace_period",
        "collateral"]
