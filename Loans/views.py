from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from PyPDF3.pdf import BytesIO
from datetime import datetime
from .process import html_to_pdf
from django.template.loader import render_to_string
from django.core.files import File
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import CreateLoanForm, AddRecordForm, AddSalesRecordForm
from .models import Beneficiaries, Loan, FinancialRecord, Record, SalesRecord, Sector, BalanceSheet
from django.utils.decorators import method_decorator


# Create your views here.
@login_required
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


@login_required
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


@login_required
def loan_details(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    data = get_stats(loan)
    return render(request, 'fsp/loan_details.html', {"loan": loan, "data": data})


@login_required
def dashboard(request):
    user = request.user
    if request.user.is_staff or request.user.is_superuser:
        loans = Loan.objects.filter(fsp=user)
        return render(request, 'fsp/fsp-home.html', {"loans": loans})
    else:
        loans = Loan.objects.all()
        return render(request, 'user/user_loan.html', {"loans": loans})


@login_required
def loans_list(request):
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    return render(request, 'fsp/loan.html', {"loans": loans})


@login_required
def fsp_profile(request):
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    return render(request, 'fsp/fsp_profile.html', {"loans": loans, "user": user})


@login_required
def loan_beneficiaries(request, pk):
    user = request.user
    loan = get_object_or_404(Loan, id=pk)
    beneficiaries = loan.beneficiaries.all()
    return render(request, 'fsp/loan_beneficiaries.html', {"user": user, "beneficiaries": beneficiaries})


def grant_loan(request):
    # TODO: grant loan tomorow
    pass


def deny_loan(request):
    # TODO: deny loan tomorow
    pass


def apply_loan(request, id):
    # TODO: apply loan tomorow
    pass


def list_of_loans(request):
    # TODO: list of users applied loans
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

        open('templates/temp.html', "w").write(render_to_string('financial-statement.html', {'f_record': f_record}))

        # getting the template
        pdf = html_to_pdf('temp.html')

        receipt_file = BytesIO(pdf.content)

        user.financial_record = File(receipt_file, "filename2.pdf")
        user.save()
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


@method_decorator(login_required, name='dispatch')
class GenerateBalanceSheet(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        b_sheet = get_object_or_404(BalanceSheet, user=user)
        f_record = get_object_or_404(FinancialRecord, user=user)

        today = datetime.today()

        total_capital = b_sheet.total_capital
        total_equity = b_sheet.get_total_equity()
        b_sheet.total_equity = total_equity
        total_liabilities = b_sheet.get_total_liabilities()
        b_sheet.total_liabilities = total_liabilities
        total_assets = b_sheet.get_total_assets()
        b_sheet.total_assets = total_assets

        retained_earnings = b_sheet.get_retained_earnings(f_record.get_total_incomes)
        equity_and_liability = b_sheet.get_equity_and_liability()

        cash_dividend = b_sheet.cash_dividend
        stock_dividend = b_sheet.stock_dividend
        liabilities = b_sheet.liabilities
        assets = b_sheet.assets

        # b_sheet.save()

        name = user.username + " " + " Company"

        open('templates/temp2.html', "w").write(render_to_string('balance-sheet.html',
                                                                 {'b_sheet': b_sheet,
                                                                  'liabilities': liabilities.all(),
                                                                  'name': name,
                                                                  'assets': assets.all(),
                                                                  'today': today,
                                                                  'total_capital': total_capital,
                                                                  'retained_earnings': retained_earnings,
                                                                  'total_equity': total_equity,
                                                                  'total_liabilities': total_liabilities,
                                                                  'total_assets': total_assets,
                                                                  'equity_and_liability': equity_and_liability,
                                                                  'cash_dividend': cash_dividend,
                                                                  'stock_dividend': stock_dividend, }))

        # getting the template
        pdf = html_to_pdf('temp2.html')

        # file_name = user.first_name + " income statement " + month + " " + year + ".pdf"
        file_name = user.username + "balance sheet" + ".pdf"

        receipt_file = BytesIO(pdf.content)

        user.balance_sheet = File(receipt_file, file_name)
        user.save()
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
