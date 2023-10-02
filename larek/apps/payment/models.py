import uuid
from datetime import datetime

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
        verbose_name="Payment Paid At",
    )

    def __str__(self):
        return f"Payment {self.id} for Order #{self.order.id}"

    class Meta:
        db_table = "payment"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    @classmethod
    def confirm_payment(cls, data: dict):
        if not (payment_id := data.get(cls.PAYMENT_ID_KWARG)):
            raise Exception
        try:
            payment = cls.objects.get(id=payment_id)
        except cls.DoesNotExist as err:
            raise Exception from err

        if payment.status != cls.STATUS_PROCESSING:
            raise Exception

        payment.paid_at = datetime.now()

        if payment.card_number == "0000 0000":
            payment.status = cls.STATUS_ERROR
        else:
            payment.status = cls.STATUS_PAID

        payment.save()
