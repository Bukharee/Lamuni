from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from multiselectfield import MultiSelectField
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import make_aware
from Users.models import Sector

# naive_datetime = datetime.now()
# naive_datetime.tzinfo
#
# settings.TIME_ZONE  # 'UTC'
# aware_datetime = make_aware(naive_datetime)
# aware_datetime.tzinfo  # <UTC>
#
# print(aware_datetime.tzinfo)

# Create your models here.
BUSINESS_SIZE = (('MICRO', 'MICRO'), ('SMALL', 'SMALL'), ('MEDIUM', 'MEDIUM'),)


class FSP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='fsp_user')


# class FSP(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)


class Beneficiaries(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="beneficiary")
    time_applied = models.DateTimeField()
    time_payed = models.DateField()
    is_payed = models.DateTimeField()
    time_to_pay = models.DateTimeField()  # oficailly the time the loan suppose to be paid
    number_of_employee = models.PositiveIntegerField()
    is_given = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user.username)


class Loan(models.Model):
    fsp = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="fsp")
    date_created = models.DateTimeField(auto_now_add=True)
    program_title = models.CharField(max_length=200)
    size = MultiSelectField(choices=BUSINESS_SIZE, max_choices=3, max_length=100)
    sectors = models.ManyToManyField(Sector)
    amount = models.PositiveIntegerField()
    beneficiaries = models.ManyToManyField(Beneficiaries)
    is_active = models.BooleanField(default=True)
    paying_days = models.PositiveIntegerField()
    grace_period = models.PositiveIntegerField()
    collateral = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('loans:user-loan-details', args=[self.pk])

    def number_of_approved(self):
        beneficiaries = self.beneficiaries.all()
        count = 0
        for beneficiary in beneficiaries:
            if beneficiary.is_given:
                count += 1
        return count

    def number_of_yet_paid(self):
        beneficiaries = self.beneficiaries.all()
        count = 0
        for beneficiary in beneficiaries:
            if not beneficiary.is_payed:
                count += 1
        return count

    def number_of_paid(self):
        beneficiaries = self.beneficiaries.all()
        count = 0
        for beneficiary in beneficiaries:
            if beneficiary.is_payed:
                count += 1
        return count

    def get_sector_data(self):
        beneficiaries = self.beneficiaries.all()
        data = {}
        for beneficiary in beneficiaries:
            sector = beneficiary.user.sector
            it_exist = data.get(sector, 0)
            if it_exist == 0:
                data[sector] = 1
            else:
                data[sector] += 1
        return data


RECORD_CATEGORY = (('Purchase', 'Purchase'),
                   ('Expenses', 'Expenses'),
                   ('Tax', 'Tax'),
                   ('Income', 'Income'))


class Record(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=45, choices=RECORD_CATEGORY, default='', verbose_name='Category')
    description = models.CharField(max_length=40)


class SalesRecord(models.Model):
    item_name = models.CharField(max_length=200, blank=False, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cost_price_per_item = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price_per_item = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now=True)

    def get_profit(self):
        total_costs = self.quantity * self.cost_price_per_item
        total_sales = self.quantity * self.selling_price_per_item

        print('total_sales : ' + str(total_sales))
        print('self.quantity : ' + str(self.quantity))
        print('self.cost_price_per_item : ' + str(self.cost_price_per_item))
        print('self.selling_price_per_item : ' + str(self.selling_price_per_item))
        print('total_costs : ' + str(total_costs))

        return total_sales - total_costs

    @property
    def get_total_sales(self):
        total_sales = self.quantity * self.selling_price_per_item

        return total_sales

    @property
    def get_total_cost(self):
        total = self.quantity * self.cost_price_per_item

        print('get_total_cost : ' + str(total))
        return total


class FinancialRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    profit = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Profit", default=0)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    records = models.ManyToManyField(Record, blank=True)
    sales_records = models.ManyToManyField(SalesRecord, blank=True)

    def get_ideal_profit(self):

        print(self)

        profit = 0

        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        print('end date : ' + str(end_date))
        print('start date : ' + str(start_date))

        all_sales_records = self.sales_records.all()

        # print(all_sales_records)
        all_sales_records.filter(date__gte=end_date).filter(date__lte=start_date)

        for sales_record in all_sales_records.filter(date__gte=end_date).filter(date__lte=start_date):
            profit += sales_record.get_profit()
            print('get_ideal_profit : ' + str(profit))

        return profit

    @property
    def get_total_expenses(self):

        total_expenses = 0
        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        print('end date : ' + str(end_date))
        print('start date : ' + str(start_date))

        all_records = self.records.all()

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).exclude(category="Expenses"):
            total_expenses += record.amount
            print('get_total_expenses : ' + str(total_expenses))

        return total_expenses

    @property
    def total_sales(self):
        total = 0

        all_records = self.sales_records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        print('end date : ' + str(end_date))
        print('start date : ' + str(start_date))

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date):
            print(all_records)
            total += record.get_total_sales

        print('total_sales : ' + str(total))

        return total

    @property
    def get_total_incomes(self):

        total_incomes = 0
        total = 0

        all_records = self.records.all()
        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        print('end date : ' + str(end_date))
        print('start date : ' + str(start_date))

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).filter(category="Income"):
            total_incomes += record.amount
            print('income : ' + str(total_incomes))

        total = self.total_sales + total_incomes
        print("get_total_incomes : " + str(total))

        return total

    @property
    def get_total_purchase(self):

        total_purchase = 0

        all_records = self.records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        print('end date : ' + str(end_date))
        print('start date : ' + str(start_date))

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).filter(category="Purchase"):

            total_purchase += record.amount
            print('total_purchase : ' + str(total_purchase))
        return total_purchase

    @property
    def get_total_tax(self):

        total_tax = 0

        all_records = self.records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        print('end date : ' + str(end_date))
        print('start date : ' + str(start_date))

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).filter(category="Tax"):
            total_tax += record.amount
            print("tax : " + str(total_tax))

        print("get_total_tax : " + str(total_tax))
        return total_tax

    @property
    def total_costs(self):
        total = 0

        all_records = self.sales_records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        print('end date : ' + str(end_date))
        print('start date : ' + str(start_date))

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date):
            total += record.get_total_cost
            print('costs : ' + str(total))

        return total

    @property
    def get_gross_profit(self):

        """Gross profit is the profit a business makes after subtracting all the costs that are related to
        manufacturing and selling its products or services. You can calculate gross profit by deducting the cost of
        goods sold (COGS) from your total sales. """

        total = 0

        total = self.total_sales - self.total_costs

        print('get_gross_profit : ' + str(total))

        return total

    @property
    def get_net_profit(self):

        """Net profit is the amount of money your business earns after deducting all operating, interest,
        and tax expenses over a given period of time. To arrive at this value, you need to know a company’s gross
        profit. If the value of net profit is negative, then it is called net loss. """

        total = 0

        total = (self.get_gross_profit
                 + self.get_total_incomes) - (self.get_total_expenses
                                              + self.get_total_tax
                                              + self.get_total_purchase)

        print("get_net_profit : " + str(total))
        return total

    # def __str__(self) -> str:
    #     return str(self.program_title)


    # number_of_approved = loan.beneficiaries.filter(is_given=True).count()


        # Previous month stuffs

    def get_prev_ideal_profit(self):
        profit = 0

        start_date = datetime.today()
        end_date = start_date - timedelta(days=60)

        all_sales_records = self.sales_records.all()

        for sales_record in all_sales_records.filter(date__gte=end_date).filter(date__lte=start_date):
            profit += sales_record.get_profit

        return profit

    @property
    def get_prev_total_expenses(self):

        total_expenses = 0
        start_date = datetime.today()
        end_date = start_date - timedelta(days=60)

        all_records = self.records.all()

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).exclude(category="Expenses"):
            total_expenses += record.amount
        return total_expenses

    @property
    def get_prev_total_incomes(self):

        total_incomes = 0

        all_records = self.records.all()
        start_date = datetime.today()
        end_date = start_date - timedelta(days=60)

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).filter(category="Income"):
            total_incomes += record.amount
        return total_incomes

    @property
    def get_prev_total_purchase(self):

        total_purchase = 0

        all_records = self.records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=60)

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).filter(category="Purchase"):
            total_purchase += record.amount

        return total_purchase

    @property
    def get_prev_total_tax(self):

        total_tax = 0

        all_records = self.records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=60)

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date).filter(category="Tax"):
            total_tax += record.amount

        return total_tax

    @property
    def total_prev_costs(self):
        total = 0

        all_records = self.sales_records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=60)

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date):
            total += record.get_total_cost

        print("total_prev_costs : " + str(total))
        return total

    @property
    def total_prev_sales(self):
        total = 0

        all_records = self.sales_records.all()

        start_date = datetime.today()
        end_date = start_date - timedelta(days=60)

        for record in all_records.filter(date__gte=end_date).filter(date__lte=start_date):
            total += record.get_total_sales

        print("total_prev_sales : " + str(total))
        return total

    @property
    def get_prev_gross_profit(self):

        """Gross profit is the profit a business makes after subtracting all the costs that are related to
        manufacturing and selling its products or services. You can calculate gross profit by deducting the cost of
        goods sold (COGS) from your total sales. """

        total = 0

        total = self.total_prev_sales - self.total_prev_costs

        return total

    @property
    def get_prev_net_profit(self):

        """Net profit is the amount of money your business earns after deducting all operating, interest,
        and tax expenses over a given period of time. To arrive at this value, you need to know a company’s gross
        profit. If the value of net profit is negative, then it is called net loss. """

        total = 0

        total = (self.get_prev_gross_profit
                 + self.get_prev_total_incomes) - (self.get_prev_total_expenses
                                                   + self.get_prev_total_tax
                                                   + self.get_prev_total_purchase)

        return total

    @property
    def get_appreciation(self):

        """Return the company's Appreciation / Depreciation based on Profits"""

        appr = 0

        apr = self.get_net_profit - self.get_prev_net_profit

        return apr

    @property
    def get_other_incomes(self):

        total = 0

        all_records = self.records.all()
        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        other_incomes = all_records.filter(date__gte=end_date).filter(date__lte=start_date).filter(
            category="Income").filter(category="Income")

        return other_incomes

    @property
    def get_expenses(self):

        total = 0

        all_records = self.records.all()
        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        expenses = all_records.filter(date__gte=end_date).filter(date__lte=start_date).exclude(category="Income")

        return expenses
