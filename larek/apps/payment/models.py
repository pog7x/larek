import uuid

from django.db import models

from larek.apps.order.models import Order


class Payment(models.Model):
    PAYMENT_ID_KWARG = "payment_id"

    STATUS_INIT = 1
    STATUS_PROCESSING = 2
    STATUS_ERROR = 3
    STATUS_PAID = 4

    STATUSES = (
        (STATUS_INIT, "Init"),
        (STATUS_PROCESSING, "Processing"),
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
    card_number = models.TextField(
        null=True,
        blank=True,
        verbose_name="Payment Card Number",
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
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Payment Paid At",
    )

    def __str__(self):
        return f"Payment {self.id} for Order #{self.order.id}"

    class Meta:
        db_table = "payment"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def status_verbose(self):
        return dict(self.STATUSES)[self.status]

    def is_error(self):
        return self.status == self.STATUS_ERROR

    def is_paid(self):
        return self.status == self.STATUS_PAID

    def is_processing(self):
        return self.status == self.STATUS_PROCESSING

    def need_pay(self):
        return self.status in (self.STATUS_INIT, self.STATUS_ERROR)
