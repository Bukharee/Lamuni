from django.shortcuts import render
from requests import request
from .forms import CreateLoanForm
from .models import Beneficiaries

# Create your views here.

def create_loan(request):
    if request.method == "POST":
        form = CreateLoanForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.user = user
            form.save()
            # return redirect to the loan page with a message created successfully
    form = CreateLoanForm()
    return render(request, "admin/create_loan.html", {"form": form})

def loan_details(request, pk):
    pass

def grant_loan(request):
    pass

def deny_loan(request):
    pass
def apply_loan(request, id):
    pass


def list_of_loans(request):
    pass

def recommended_loans(request):
    pass
