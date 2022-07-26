from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField
from decimal import Decimal

# Create your models here.
BUSINESS_SIZE = (('MICRO', 'MICRO'), ('SMALL', 'SMALL'), ('MEDIUM', 'MEDIUM'),)


class Sector(models.Model):
    name = models.CharField(max_length=200)


class FSP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)


class Beneficiaries(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    time_applied = models.DateTimeField()
    time_payed = models.DateField()
    is_payed = models.DateTimeField()
    time_to_pay = models.DateTimeField()  # oficailly the time the loan suppose to be paid
    number_of_employee = models.PositiveIntegerField()


class Loan(models.Model):
    fsp = models.ForeignKey(FSP, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    program_title = models.CharField(max_length=200)
    size = MultiSelectField(choices=BUSINESS_SIZE, max_choices=3, max_length=100)
    sectors = models.ManyToManyField(Sector)
    amount = models.PositiveIntegerField()
    beneficiaries = models.ManyToManyField(get_user_model())
    is_active = models.BooleanField(default=True)
    paying_days = models.PositiveIntegerField()
    grace_period = models.PositiveIntegerField()
    collateral = models.CharField(max_length=200, blank=True, null=True)


RECORD_CATEGORY = (('Purchase', 'Purchase'),
                   ('Expenses', 'Expenses'),
                   ('Tax', 'Tax'),
                   ('Income', 'Income'),
                   ('Sales', 'Sales'),)


class Record(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=45, choices=RECORD_CATEGORY, default='', verbose_name='Category')


class SalesRecord(models.Model):
    item_name = models.TextField(max_length=200, blank=False, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cost_price_per_item = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price_per_item = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class FinancialRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    profit = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Profit", default=0)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    records = models.ManyToManyField(Record, blank=True)
    sales_records = models.ManyToManyField(SalesRecord, blank=True)

    # @property
    # def get_net_profit(self):
    #     net_amount_spend = 0.00  # all record entries which are not Income
    #     monthly_capital = self.monthly_capital
    #     all_records = self.records.all()
    #
    #     for record in all_records:
    #         if record.category != "Income":
    #             net_amount_spend += record.amount
    #
    #     for record in all_records:
    #         # add an Income to monthly profit
    #         if record.category == "Income":
    #             monthly_capital += record.amount
    #
    #     net_profit = monthly_capital - net_amount_spend
    #
    #     return net_profit
