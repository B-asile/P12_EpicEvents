from django.db import models
from users.models import User
from customers.models import Customer


class Event(models.Model):
    choice_status = [
        ('open', 'OPEN'),
        ('close', 'CLOSED'),
    ]
    event_name = models.CharField(max_length=1024)
    event_status = models.CharField(max_length=64, choices=choice_status)
    event_date = models.DateField(null=True)
    created_date = models.DateField(null=True)
    updated_date = models.DateField(null=True)
    attendees = models.PositiveSmallIntegerField(null=True)
    note = models.TextField()
    company_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='event_company_name')
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_sales_contact')
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_contact_support', null=True,
                                        blank=True, default=None,)

    def __str__(self):
        return f"Event #{self.pk} - {self.event_name}"