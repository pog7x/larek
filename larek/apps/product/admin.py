from django.contrib import admin

from larek.apps.product.models import (
    Product,
    ProductImage,
    Characteristic,
    ProductCharacteristic,
)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Characteristic)
admin.site.register(ProductCharacteristic)
