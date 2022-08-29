from django.core.mail import EmailMessage
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from datetime import datetime, timedelta
from PyPDF3.pdf import BytesIO
from datetime import datetime
from .process import html_to_pdf
from django.template.loader import render_to_string
from django.core.files import File
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CreateLoanForm, AddRecordForm, AddSalesRecordForm, ApplyLoanForm
from .models import Beneficiaries, Loan, FinancialRecord, Record, SalesRecord, Sector, BalanceSheet, Payment
from django.utils.decorators import method_decorator
from django.db.models import Q
from Users.models import User
import json
import requests
from django.conf import settings


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


def get_stats_all(loans):
    number_of_approved = 0
    amount_given = 0
    for loan in loans:
        number_of_approved += loan.number_of_approved()

    data = {
        "number_of_approved": number_of_approved,

    }
    return data


def loan_details(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    data = get_stats(loan)
    return render(request, 'fsp/loan_details.html', {"loan": loan, "data": data})


@login_required
def user_loan_details(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    return render(request, 'user/user_loan_details.html', {"loan": loan})


@login_required
def dashboard(request):
    user = request.user
    loans = Loan.objects.filter(fsp=user)
    if request.user.is_staff or request.user.is_superuser:
        loans = Loan.objects.filter(fsp=user)
        data = get_stats_all(loans)
        return render(request, 'fsp/fsp-home.html', {"loans": loans, "data": data})
    else:
        loans = Loan.objects.all()
        return render(request, 'user/user_loan.html', {"loans": loans})


@login_required
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
    return render(request, 'fsp/loan_beneficiaries.html', {"user": user, "beneficiaries": beneficiaries})


def grant_loan(request, loan_id, username):
    # TODO: grant loan tomorow test
    # take the user
    user = get_object_or_404(User, username=username)
    print(user.username)
    loan = get_object_or_404(Loan, id=loan_id)
    is_granted = loan.grant_loan(user)
    if is_granted:
        return JsonResponse({"message": "granted"}, status=200)
    return JsonResponse({"message": "not an applicant"}, status=403)
    # and will never apply to this specific loan program again


def deny_loan(request, loan_id, username):
    # TODO: deny loan tomorow test
    user = get_object_or_404(User, username=username)
    loan = get_object_or_404(Loan, id=loan_id)
    is_denied = loan.deny_loan(user)
    if is_denied:
        return JsonResponse({"mesage": "denied"}, status=200)
        # send the user a sorry message that this isnt the right program for him
    return JsonResponse({"message": "not applicant"}, status=403)


def apply_loan(request, id):
    # TODO: apply loan tomorow continue
    # user cannot apply loan if theres an outstanding loan payment
    user = request.user
    applications = Beneficiaries.objects.filter(Q(user=user) | Q(is_given=True))
    loan = get_object_or_404(Loan, id=id)
    form = ApplyLoanForm(user=user, loan_id=id, data=request.GET)
    if request.method == "POST":
        form = ApplyLoanForm(user=user, loan_id=id, data=request.POST)
        print(form)
        if not applications.exists():
            if form:
                print(form, "the incredible form")
                if form.is_valid():
                    # TODO: write a better eligibility function here current only checks
                    # if the user have ever applied to the particular loan program what if the whole
                    # program was renewed and he wants to apply again
                    beneficiary = Beneficiaries.objects.create(user=user, number_of_employee=int(
                        form.cleaned_data["number_of_employee"]) if not \
                        (user.number_of_employee) else user.number_of_employee)
                    loan.beneficiaries.add(beneficiary)
                    generate_balance_sheet(request.user, True)
                    generate_income_statement(request,user, True)
                    return render(request, "apply_message.html", {"message": \
                                                                      "successfully applied!, you'll hear from us sonn"})
                return render(request, "apply_message.html", {"user": user, "message": \
                    "Sorry we cannot offer you Credit!, Try Again"})
        return render(request, "apply_message.html", {"message": "You Have Already Applied to this program!"})
    else:
        return render(request, "apply_for_loan.html", {"form": form})

    # if the user credit score is below 50% dont give him
    # if the user has no problem
    # add him to the beneficiaries list
    # with all his documents and things


def users_credentials(request, loan_id):
    """This will query all the requirements of a user of the particular loan"""
    user = request.user
    loan = get_object_or_404(Loan, id=loan_id)
    output = {}
    for requirement in loan.requirements.all():
        print(requirement.requiremenent)
        output[requirement.requiremenent] = getattr(user, requirement.requiremenent)
    print(output)
    return render(request, "users_credentials.html", {"credentials": output})


def recommended_loans(request):
    # TODO: recommend loan
    # check the loans that target the bussiness size and sector to be top
    user = request.user
    recommended = Loan.objects.filter(Q(sector=user.sector, size=user.size) |
                                      Q(size=user.size) | Q(sector=user.sector))
    # call a fake machine learning recomendation algorithm
    return render(request, "recommended_loans.html", {"loans": recommended})


def search(request):
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
            f_record.records.add(record)
            return redirect("users:profile")

    else:
        add_record_form = AddRecordForm()

    context = {
        'form': add_record_form
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
            return redirect("users:profile")
        else:
            print(add_sales_form.errors)

    else:
        add_sales_form = AddSalesRecordForm()

    context = {
        'form': add_sales_form
    }
    return render(request, 'add_sales_record.html', context)


def fs(request):
    user = request.user
    f_record = get_object_or_404(FinancialRecord, user=user)
    print(f_record.get_ideal_profit)


def fr(request, pk):
    record = get_object_or_404(SalesRecord, pk=pk)
    print(record.get_profit)  #


@login_required()
def generate_income_statement(user, is_apply_loan):
    f_record = get_object_or_404(FinancialRecord, user=user)
    records = f_record.records
    other_income = f_record.get_other_incomes
    total_sales = f_record.total_sales
    total_income = f_record.get_total_incomes
    expenses = f_record.get_expenses
    total_expenses = f_record.get_total_expenses

    start_date = datetime.today()
    end_date = start_date - timedelta(days=30)
    revenues = f_record.total_sales
    prev_revenues = f_record.total_prev_sales
    net_profit = f_record.get_net_profit
    prev_net_profit = f_record.get_prev_net_profit
    ideal_profit = f_record.get_ideal_profit()
    print(str(ideal_profit))

    gross_profit = f_record.get_gross_profit
    prev_gross_profit = f_record.get_prev_gross_profit

    depreciation = f_record.get_appreciation

    f_record.revenue = revenues
    f_record.net_profit = net_profit
    f_record.profit = gross_profit
    f_record.save()

    try:
        depreciation_percent = (net_profit / prev_net_profit) * 100

    except ZeroDivisionError:

        depreciation_percent = 0

    name = user.username + " " + " Company"

    open('templates/temp.html', "w").write(render_to_string('income-statement.html',
                                                            {'f_record': f_record,
                                                             'records': records,
                                                             'name': name,
                                                             'from_date': end_date,
                                                             'to_date': start_date,
                                                             'revenues': revenues,
                                                             'net_profit': net_profit,
                                                             'gross_profit': gross_profit,
                                                             'depreciation': depreciation,
                                                             'prev_revenues': prev_revenues,
                                                             'prev_net_profit': prev_net_profit,
                                                             'prev_gross_profit': prev_gross_profit,
                                                             'depreciation_percent': depreciation_percent,
                                                             'other_incomes': other_income,
                                                             'total_sales': total_sales,
                                                             'total_income': total_income,
                                                             'expenses': expenses,
                                                             'total_expenses': total_expenses, }))

    # getting the template
    pdf = html_to_pdf('temp.html')

    # file_name = user.first_name + " income statement " + month + " " + year + ".pdf"
    file_name = user.username + " income statement" + ".pdf"

    receipt_file = BytesIO(pdf.content)

    user.financial_record = File(receipt_file, file_name)
    user.save()
    # rendering the template
    # return HttpResponse(pdf, content_type='application/pdf')
    if not is_apply_loan:
        return receipt_file


@login_required()
def generate_balance_sheet(user, is_apply_loan):
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
    # return HttpResponse(pdf, content_type='application/pdf')

    if not is_apply_loan:
        return receipt_file


@login_required
def request_financial_statements(request):
    user = request.user

    headers = {
        "Authorization": "dskjdks",
        "Content-Type": "application/json",
        "sandbox-key": settings.SANDBOX_KEY
    }
    url = "https://fsi.ng/api/v1/flutterwave/v3/virtual-account-numbers"
    data = ({
        "email": user.email,
        "is_permanent": True,
        "bvn": user.bvn,
        "amount": 500,
        "phonenumber": user.phone,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "narration": "Lamuni",
    })

    my_data = requests.post(url=url, json=data, headers=headers)

    if my_data.status_code not in [200, 203]:
        message = "There was an error creating account number : {}:{}".format(
            my_data.status_code, my_data.text
        )
        print(message)

        data = {
            "message": message
        }
        return render(request, 'add_sales_record.html', context=data)

    json_data = my_data.json()

    real_data = json_data['data']

    account_number = real_data['account_number']
    message = real_data['note']
    bank = real_data['bank_name']
    tx_ref = real_data['flw_ref']

    payment = Payment.objects.create(
        user=user,
        tx_ref=tx_ref,
        account_number=account_number,
        account_name=message,
    )

    data = {
        "note": message,
        "account_number": account_number,
        "tx_ref": tx_ref,
        "bank_name": bank,
        "message": "Transfer the money to the above account number whenever receive your payment, your financial "
                   "statement will be sent to your email "
    }

    return render(request, 'add_sales_record.html', context=data)


def verify_transfer(request):

    """Webhook to verify any transfer made to Flutterwave and send the two pdf files to the user. This is an
    automatic process"""

    headers = {
        "Authorization": "dskjdks",
        "Content-Type": "application/json",
        "sandbox-key": settings.SANDBOX_KEY
    }
    response = requests.get("https://lamuni.com.ng/payments/transfer/verify", headers=headers)
    tx_ref = response.headers.get("tx_ref")
    payment = Payment.objects.get(tx_ref=tx_ref)

    if response.data.status == "successful" & response.data.amount == payment.amount:
        pdf = generate_income_statement(payment.user, False)
        filename = 'Income Statement.pdf'
        to_email = [payment.user.email]
        subject = "Your Financial Record from Lamuni"
        body = "Hello, After verifying your transfer attached is your Income Statement"
        email = EmailMessage(subject=subject, body=body, from_email="test@lamuni.com.ng", to=to_email)
        email.attach(filename, pdf, "application/pdf")
        email.send(fail_silently=True)

        pdf_2 = generate_balance_sheet(payment.user, False)
        filename_2 = 'Balance Sheet.pdf'
        subject_2 = "Your Financial Record from Lamuni"
        body_2 = "Hello, After verifying your transfer attached is your Balance Sheet"
        email_2 = EmailMessage(subject=subject_2, body=body_2, from_email="test@lamuni.com.ng", to=to_email)
        email_2.attach(filename_2, pdf_2, "application/pdf")
        email_2.send(fail_silently=True)

    return HttpResponse(status=200)
