from django.db import models
from users.models import User


class Customer(models.Model):
    company_name = models.CharField(max_length=1024, unique=True)
    address = models.CharField(max_length=1024)
    transformed = models.BooleanField(default=False)
    contact_name = models.CharField(max_length=1024, unique=True)
    contact_phone = models.CharField(max_length=15, unique=True)
    contact_job = models.CharField(max_length=1024)
    contact_email = models.EmailField(unique=True)
    comments = models.TextField(blank=True)
    sales_contact = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='contract_sales_contact',
    )

    def __str__(self):
        return self.company_name