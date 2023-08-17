from django.contrib import admin

from larek.apps.product.models import Product, ProductImage

admin.site.register(Product)
admin.site.register(ProductImage)
