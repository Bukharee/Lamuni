from django.shortcuts import redirect, render, get_object_or_404
from .forms import CreateLoanForm
from .models import Beneficiaries, Loan, Sector
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
            return redirect('loans:loan_details', pk=form.id)
    form = CreateLoanForm()
    sectors = Sector.objects.all()
    return render(request, "fsp/create_loan.html", {"form": form, "sectors": sectors})


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
    return render(request, 'fsp/fsp-home.html', {"loans": loans})


def loans_list(request):
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    return render(request, 'fsp/loan.html', {"loans": loans})


def fsp_profile(request):
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    return render(request, 'fsp/fsp_profile.html', {"loans": loans, "user": user})


def loan_beneficiaries(request, pk):
    user = request.user
    loan = get_object_or_404(Loan, id=pk)
    beneficiaries = loan.beneficiaries.all()
    return render(request, 'fsp/loan_beneficiaries.html', {"user": user, "beneficiaries": beneficiaries})


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
