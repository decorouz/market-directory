from django.contrib import admin
from django.db.models import Count, Avg
from django.utils.html import format_html
from django.utils.http import urlencode

from django.urls import reverse
from .models import (
    Commodity,
    Category,
    ContactPerson,
    Market,
    AcceptedPaymentMethod,
    MarketCommodity,
)
from datetime import date, timedelta


@admin.register(AcceptedPaymentMethod)
class AcceptablePaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("type", "charges")
    list_editable = ("charges",)


@admin.register(MarketCommodity)
class MarketCommodityAdmin(admin.ModelAdmin):
    autocomplete_fields = ("market", "commodity")
    list_display = (
        "market_date",
        "market",
        "commodity",
        "commodity_price",
    )
    list_select_related = ("market", "commodity")
    search_fields = ("commodity__name__istartswith",)


class MarketCommodityInline(admin.TabularInline):
    model = MarketCommodity
    extra = 2


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    autocomplete_fields = ("contact_person",)
    list_display = (
        "name",
        "country",
        "brief_detail",
        "num_vendor",
        "contact_person",
        "market_days_interval",
        "reference_mkt_date",
        "next_market_date",
        "is_active",
        "status",
    )
    list_select_related = ("contact_person",)
    list_per_page = 5

    search_fields = ("name__istartswith",)

    @admin.display(ordering="reference_mkt_date")
    def next_market_date(self, market):
        today = date.today()
        ref_date = market.reference_mkt_date
        interval = market.market_days_interval

        while ref_date <= today:
            ref_date = ref_date + timedelta(interval)
        return ref_date


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "commodities_count")

    @admin.display(ordering="commodities_count")
    def commodities_count(self, category):
        url = (
            reverse("admin:markets_commodity_changelist")
            + "?"
            + urlencode({"category__id": str(category.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, category.commodities_count)

    def get_queryset(self, request):
        return (
            super().get_queryset(request).annotate(commodities_count=Count("commodity"))
        )


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "market_count",
    )
    list_per_page = 10
    search_fields = ("first_name__istartswith",)

    @admin.display(ordering="market_count")
    def market_count(self, contact_person):
        url = (
            reverse("admin:markets_market_changelist")
            + "?"
            + urlencode({"contact_person_id": str(contact_person.id)})
        )
        return format_html(
            "<a href='{}'>{} markets</a>", url, contact_person.market_count
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(market_count=Count("market"))


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = (
        "custom_name",
        "local_name",
        "overview",
        "category",
        "grade",
    )
    search_fields = ("name",)
    list_per_page: int = 10

    def custom_name(self, commodity: Commodity):
        if commodity.grade:
            return f"{commodity.grade}-{commodity.name}"
        return f"{commodity.name}"
