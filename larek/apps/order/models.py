from django.db import models

from larek.apps.delivery.models import Delivery
from larek.apps.user.models import User


class Order(models.Model):
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
    city_to = models.TextField(max_length=30, null=True, verbose_name="Order City")
    address_to = models.TextField(
        max_length=30, null=True, verbose_name="Order Address"
    )
    created_at = models.DateTimeField(null=True, verbose_name="Order Created At")

    def __str__(self):
        return f"Order #{self.id}"

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
