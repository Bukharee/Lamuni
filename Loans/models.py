from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField
from Users.models import Sector

# Create your models here.
BUSSINESS_SIZE = (('MICRO', 'MICRO'),('SMALL', 'SMALL'),('MEDIUM', 'MEDIUM'),)


  

# class FSP(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)

class Beneficiaries(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="beneficiary")
    time_applied = models.DateTimeField()
    time_payed = models.DateField()
    is_payed = models.DateTimeField()
    time_to_pay = models.DateTimeField() #oficailly the time the loan suppose to be paid
    number_of_employee = models.PositiveIntegerField()
    is_given = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user.username)
    

    
class Loan(models.Model):
    fsp = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="fsp")
    date_created = models.DateTimeField(auto_now_add=True)
    program_title = models.CharField(max_length=200)
    size = MultiSelectField(choices=BUSSINESS_SIZE, max_choices=3, max_length=100)
    sectors = models.ManyToManyField(Sector)
    amount = models.PositiveIntegerField()
    beneficiaries = models.ManyToManyField(get_user_model())
    is_active = models.BooleanField(default=True)
    paying_days = models.PositiveIntegerField()
    grace_period = models.PositiveIntegerField()
    collateral = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.program_title)

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
    
    # number_of_approved = loan.beneficiaries.filter(is_given=True).count()

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