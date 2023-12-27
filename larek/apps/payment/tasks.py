from celery import shared_task
from django.db import transaction
from django.utils import timezone

from larek.apps.cart.models import Cart
from larek.apps.order.models import Order
from larek.apps.payment.models import Payment
from larek.apps.product_seller.models import ProductSeller


@shared_task
def confirm_payment(payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        order = Order.objects.get(id=payment.order.id)
    except Payment.DoesNotExist as err:
        raise Exception from err

    if payment.status != Payment.STATUS_PROCESSING:
        raise Exception

    with transaction.atomic():
        if payment.card_number == "0000 0000":
            payment.status = Payment.STATUS_ERROR
            order.status = Order.STATUS_PAYMENTS_ERROR
        else:
            payment.paid_at = timezone.now()
            payment.status = Payment.STATUS_PAID
            order.status = Order.STATUS_COMPLETED

        payment.save()
        order.save()

        ProductSeller.decrease_products_count(order_id=order.id)
        Cart.decrease_products_count(order_id=order.id)
