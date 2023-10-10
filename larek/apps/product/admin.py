from django.contrib import admin

from larek.apps.product.models import (
    Characteristic,
    Product,
    ProductCharacteristic,
    ProductImage,
)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Characteristic)
admin.site.register(ProductCharacteristic)
