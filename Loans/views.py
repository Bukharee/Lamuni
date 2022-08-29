from datetime import timezone
from traceback import print_tb
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from PyPDF3.pdf import BytesIO
from .process import html_to_pdf
from django.template.loader import render_to_string
from django.core.files import File
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CreateLoanForm, AddRecordForm, AddSalesRecordForm, ApplyLoanForm
from .models import Beneficiaries, Loan, FinancialRecord, Record, SalesRecord,  Sector
from django.utils.decorators import method_decorator
from django.db.models import Q
from Users.models import User

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
            "number_of_approved": number_of_approved, "sectors_count": sectors_count,
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
    """All list Of Loans that the Fspo has created"""
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    return render(request, 'fsp/loan.html', {"loans": loans})

def list_loans(request):
    """All the list of loans from all financial service providers"""
    loans = Loan.objects.all()
    print(loans)
    return render(request, "list_of_loans.html", {"loans": loans})

def fsp_profile(request):
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    return render(request, 'fsp/fsp_profile.html', {"loans": loans, "user": user})


def loan_beneficiaries(request, pk):
    user = request.user
    loan = get_object_or_404(Loan, id=pk)
    beneficiaries = loan.beneficiaries.all()
    print(beneficiaries)
    return render(request, 'fsp/loan_beneficiaries.html', {"user": user, "beneficiaries": beneficiaries})



def grant_loan(request, loan_id, username):
    # TODO: grant loan tomorow test
    #take the user
    user = get_object_or_404(User, username=username)
    print(user.username)
    loan = get_object_or_404(Loan, id=loan_id)
    is_granted = loan.grant_loan(user)
    if is_granted:
        return JsonResponse({"message": "granted"}, status=200)
    return JsonResponse({"message": "not an applicant"}, status=403)
    #and will never apply to this specific loan program again


def deny_loan(request, loan_id, username):
    # TODO: deny loan tomorow test
    user = get_object_or_404(User, username=username)
    loan = get_object_or_404(Loan, id=loan_id)
    is_denied = loan.deny_loan(user)
    if is_denied:    
        return JsonResponse({"mesage":"denied"}, status=200)
        # send the user a sorry message that this isnt the right program for him 
    return JsonResponse({"message": "not applicant"}, status=403)


def apply_loan(request, id):
    # TODO: apply loan tomorow continue
    #user cannot apply loan if theres an outstanding loan payment
    user = request.user
    applications = Beneficiaries.objects.filter(Q(user=user) | Q(is_given=True))
    loan = get_object_or_404(Loan, id=id)
    form = ApplyLoanForm(user=user, loan_id=id, data=request.GET)
    if request.method == "POST":
        form  =  ApplyLoanForm(user=user, loan_id=id, data=request.POST)
        print(form)
        if  not applications.exists():
            if form:
                print(form, "the incredible form")
                if form.is_valid():
                    #TODO: write a better eligibility function here current only checks 
                    # if the user have ever applied to the particular loan program what if the whole
                    #program was renewed and he wants to apply again
                    beneficiary = Beneficiaries.objects.create(user=user, number_of_employee= int(form.cleaned_data["number_of_employee"]) if not  \
                    (user.number_of_employee) else user.number_of_employee)
                    loan.beneficiaries.add(beneficiary)
                    return render(request, "apply_message.html", {"message": \
                    "successfully applied!, you'll hear from us sonn"})
                return render(request, "apply_message.html", {"user": user, "message": \
                    "Sorry we cannot offer you Credit!, Try Again"})
        return render(request, "apply_message.html", {"message": "You Have Already Applied to this program!"})
    else:
        return render(request, "apply_for_loan.html", {"form": form})
        
    #if the user credit score is below 50% dont give him 
    #if the user has no problem 
    #add him to the beneficiaries list
    #with all his documents and things 

def users_credentials(request, loan_id, username):
    """This will query all the requirements of a user of the particular loan"""
    user = get_object_or_404(User, username=username)
    loan = get_object_or_404(Loan, id=loan_id)
    output = {}
    for requirement in loan.requirements.all():
        print(requirement.requiremenent)
        output[requirement.requiremenent] = getattr(user, requirement.requiremenent)
    print(output)
    return render(request, "users_credentials.html", {"credentials": output})



def recommended_loans(request):
    #TODO: recommend loan
    #check the loans that target the bussiness size and sector to be top
    user = request.user
    recommended = Loan.objects.filter(Q(sector=user.sector, size=user.size) | 
    Q(size=user.size) | Q(sector=user.sector))
    #call a fake machine learning recomendation algorithm
    return render(request, "recommended_loans.html", {"loans": recommended})



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


@login_required()
def add_sales_record(request):
    user = request.user

    try:

        f_record = FinancialRecord.objects.get(user=user)

    except Exception:

        f_record = FinancialRecord.objects.create(user=user)

    if request.method == "POST":
        add_sales_form = AddSalesRecordForm(request.POST)
        if add_sales_form.is_valid():
            name = add_sales_form.cleaned_data['item_name']
            quantity = add_sales_form.cleaned_data['quantity']
            cost_price = add_sales_form.cleaned_data['cost_price_per_item']
            sales_price = add_sales_form.cleaned_data['selling_price_per_item']
            record = SalesRecord.objects.create(item_name=name,
                                                quantity=quantity,
                                                cost_price_per_item=cost_price,
                                                selling_price_per_item=sales_price)
            f_record.sales_records.add(record)
            return HttpResponseRedirect('/accounts/user_profile/')

    else:
        add_sales_form = AddSalesRecordForm()

    context = {
        'add_sales_form': add_sales_form
    }
    return render(request, 'add_sales_record.html', context)


def fs(request):
    user = request.user
    f_record = get_object_or_404(FinancialRecord, user=user)
    print(f_record.get_ideal_profit)


def fr(request, pk):
    record = get_object_or_404(SalesRecord, pk=pk)
    print(record.get_profit)  #


@method_decorator(login_required, name='dispatch')
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        f_record = get_object_or_404(FinancialRecord, user=user)

        open('templates/temp.html', "w").write(render_to_string('result.html', {'f_record': f_record}))

        # getting the template
        pdf = html_to_pdf('temp.html')

        receipt_file = BytesIO(pdf.content)

        user.financial_record = File(receipt_file, "filename2.pdf")
        user.save()
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
