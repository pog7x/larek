from django.db import models

from larek.apps.order.models import Order


class Payment(models.Model):
    order = models.ForeignKey(
        to=Order,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Order",
        related_name="payment",
    )
    sum = models.FloatField(
        default=0,
        null=True,
        verbose_name="Payment Sum",
    )
    status = models.TextField(
        max_length=30,
        null=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(null=True, verbose_name="Payment Created At")

    class Meta:
        db_table = "payment"
