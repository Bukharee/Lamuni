from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateLoanForm
from .models import Beneficiaries, FinancialRecord, Record
from django.contrib.auth.decorators import login_required
from .forms import AddRecordForm


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


@login_required()
def add_record(request):
    user = request.user

    try:

        f_record = FinancialRecord.objects.get(user=user)

    except Exception:

        f_record = FinancialRecord.objects.create(user=user)

    if request.method == "POST":
        add_record_form = AddRecordForm(request.POST)
        if add_record_form.is_valid():
            amount = add_record_form.cleaned_data['amount']
            category = add_record_form.cleaned_data['category']
            record = Record.objects.create(amount=amount, category=category)
            f_record.record.add(record)
            return HttpResponseRedirect('/accounts/user_profile/')

    else:
        add_record_form = AddRecordForm()

    context = {
        'add_record_form': add_record_form
    }
    return render(request, 'add_record.html', context)
