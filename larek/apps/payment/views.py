from rest_framework import viewsets

from larek.apps.payment.models import Payment
from larek.apps.payment.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
