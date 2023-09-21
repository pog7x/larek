import uuid

from django.db import models

from larek.apps.order.models import Order


class Payment(models.Model):
    STATUS_INIT = 1
    STATUS_ERROR = 2
    STATUS_PAID = 3

    STATUSES = (
        (STATUS_INIT, "Init"),
        (STATUS_ERROR, "Error"),
        (STATUS_PAID, "Paid"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    order = models.ForeignKey(
        to=Order,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Payment Order",
        related_name="payment",
    )
    sum = models.FloatField(
        default=0,
        null=True,
        verbose_name="Payment Sum",
    )
    status = models.IntegerField(
        null=True,
        blank=True,
        choices=STATUSES,
        default=STATUS_INIT,
        verbose_name="Payment Status",
    )
    created_at = models.DateTimeField(
        null=True,
        auto_now_add=True,
        verbose_name="Payment Created At",
    )

    def __str__(self):
        return f"Payment {self.id} for Order #{self.order.id}"

    class Meta:
        db_table = "payment"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
