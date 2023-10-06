from rest_framework import viewsets
from rest_framework.response import Response
from larek.apps.product.models import Product
from larek.apps.views_history.models import ViewsHistory
from larek.apps.product.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related(
        "product_seller", "review", "product_characteristic"
    )
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.set_views_history(instance=instance)
        return Response(serializer.data)

    def set_views_history(self, instance):
        views, created = ViewsHistory.objects.get_or_create(
            product_id=instance.id,
            user_id=self.request.user.id or None,
        )

        if not created:
            views.count += 1
            views.save()
