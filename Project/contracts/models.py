from django.db import models
from customers.models import Customer
from users.models import User


class Contract(models.Model):
    choice_status = [
        ('open', 'OPEN'),
        ('signed', 'SIGNED'),
    ]
    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)
    commitments = models.CharField(max_length=1024)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due =  models.DateField(null=True)
    contract_status = models.CharField(max_length=64, choices=choice_status)
    company_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contract_company_name')
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contract_sales_contact')

    def __str__(self):
        return "Contrat num. {}".format(str(self.pk))