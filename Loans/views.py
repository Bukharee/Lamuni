from django.shortcuts import redirect, render, get_object_or_404
from .forms import CreateLoanForm
from .models import Beneficiaries, Loan
from django.db.models import Count


# Create your views here.

def create_loan(request):
    if request.method == "POST":
        form = CreateLoanForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.fsp = user
            form.save()
            return redirect('loan_details', pk=form.id)
    form = CreateLoanForm()
    print(form, "form")
    return render(request, "fsp/create_loan.html", {"form": form})


def get_stats(loan):
    number_of_applicants = loan.beneficiaries.count()
    number_of_approved = loan.number_of_approved()
    sectors_count = loan.get_sector_data()
    number_of_yet_paid = loan.number_of_yet_paid()
    number_of_paid = loan.number_of_paid()
    data = {"number_of_applicants": number_of_applicants, 
    "number_of_approved": number_of_approved, "sectors_count":sectors_count, 
    "number_of_yet_paid": number_of_yet_paid, "number_of_paid": number_of_paid}
    return data


def loan_details(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    data = get_stats(loan)
    return render(request, 'fsp/loan_details.html', {"loan": loan, "data": data})
    

def dashboard(request):
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    return render(request, 'fsp/dashboard.html', {"loans": loans})

def grant_loan(request):
    #TODO: grant loan tomorow
    pass

def deny_loan(request):
    #TODO: deny loan tomorow
    pass

def apply_loan(request, id):
    #TODO: apply loan tomorow
    pass


def list_of_loans(request):
    #TODO: list of users applied loans
    pass

def recommended_loans(request):
    pass
