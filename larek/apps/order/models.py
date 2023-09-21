from django.db import models

from larek.apps.delivery.models import Delivery
from larek.apps.user.models import User


class Order(models.Model):
    STATUS_CREATED = 1
    STATUS_PAYMENTS_ERROR = 2
    STATUS_COMPLETED = 3

    STATUSES = (
        (STATUS_CREATED, "Created"),
        (STATUS_PAYMENTS_ERROR, "Payment error"),
        (STATUS_COMPLETED, "Completed"),
    )

    full_name = models.TextField(
        max_length=150,
        null=True,
        verbose_name="Order Full Name",
    )
    phone = models.TextField(
        null=True,
        blank=True,
        verbose_name="Order Phone",
    )
    email = models.EmailField(
        null=True,
        blank=True,
    )
    delivery = models.ForeignKey(
        to=Delivery,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Order Delivery",
        related_name="order",
    )
    user = models.ForeignKey(
        to=User,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Order User",
        related_name="order",
    )
    address = models.TextField(
        max_length=300,
        null=True,
        verbose_name="Order Address",
    )
    created_at = models.DateTimeField(
        null=True,
        auto_now_add=True,
        verbose_name="Order Created At",
    )
    status = models.IntegerField(
        null=True,
        blank=True,
        choices=STATUSES,
        default=STATUS_CREATED,
        verbose_name="Order Status",
    )

    def __str__(self):
        return f"Order #{self.id}"

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
