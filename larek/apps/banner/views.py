import logging
from datetime import datetime
from typing import Any

from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from larek.apps.banner.models import Banner

logger = logging.getLogger(__name__)


class BannerListView(ListView):
    model = Banner
    template_name = "index.html"
    context_object_name = "banners"

    def get_queryset(self) -> QuerySet[Any]:
        qs = self.model.objects.prefetch_related("product_seller").filter(
            expired_at__gt=datetime.now(),
        )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        if not (banners := ctx.get(self.context_object_name)):
            return ctx

        main_slider, limited_offers, popular_goods, limited_edition = [], [], [], []

        for banner in banners:
            if banner.is_main_slider:
                main_slider.append(banner)
            elif banner.is_limited_offers:
                limited_offers.append(banner)
            elif banner.is_popular_goods:
                popular_goods.append(banner)
            elif banner.is_limited_edition:
                limited_edition.append(banner)

        ctx["main_slider"] = main_slider
        ctx["limited_offers"] = limited_offers[:1]
        ctx["popular_goods"] = popular_goods
        ctx["limited_edition"] = limited_edition

        return ctx
