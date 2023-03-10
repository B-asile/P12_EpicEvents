# Generated by Django 4.1.6 on 2023-02-06 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=1024, unique=True)),
                ("address", models.CharField(max_length=1024)),
                ("transformed", models.BooleanField(default=False)),
                ("contact_name", models.CharField(max_length=1024, unique=True)),
                ("contact_phone", models.CharField(max_length=15, unique=True)),
                ("contact_job", models.CharField(max_length=1024)),
                ("contact_email", models.EmailField(max_length=254, unique=True)),
                ("comments", models.TextField(blank=True)),
                (
                    "sales_contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_sales_contact",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
