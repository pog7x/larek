from django.db import models


class Delivery(models.Model):
    price = models.FloatField(
        default=0,
        null=True,
        verbose_name="Price",
    )
    order_sum = models.FloatField(
        default=0,
        null=True,
        verbose_name="Order Sum",
    )
    verbose = models.TextField(
        null=True,
        verbose_name="Verbose",
    )

    class Meta:
        db_table = "delivery"
