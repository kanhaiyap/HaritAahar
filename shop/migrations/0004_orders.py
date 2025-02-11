# Generated by Django 4.2.5 on 2025-01-08 16:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0003_alter_order_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
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
                ("customer_name", models.CharField(max_length=100)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[("paid", "Paid"), ("unpaid", "Unpaid")], max_length=20
                    ),
                ),
                ("is_fulfilled", models.BooleanField(default=False)),
                (
                    "issue_status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("resolved", "Resolved")],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
