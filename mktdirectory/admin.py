from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode

from django.urls import reverse
from .models import (
    Commodity,
    Category,
    ContactPerson,
    Market,
    AcceptedPaymentMethod,
    MarketDay,
)
from datetime import date, timedelta


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ("name", "overview", "category")
    list_per_page: int = 10
    list_editable = ("category",)


@admin.register(AcceptedPaymentMethod)
class AcceptablePaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("type", "charges")
    list_editable = ("charges",)


@admin.register(MarketDay)
class MarketDayAdmin(admin.ModelAdmin):
    list_display = (
        "market_date",
        "market",
        "commodity",
        "grade",
        "commodity_price",
    )
    list_select_related = ("market", "commodity")
    list_editable = ("grade", "commodity_price")


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brief_details",
        "num_vendors",
        "contact_person",
        "market_days_interval",
        "reference_mkt_date",
        "next_market_date",
    )
    list_select_related = ("contact_person",)
    list_per_page = 5

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
            reverse("admin:mktdirectory_commodity_changelist")
            + "?"
            + urlencode({"category__id": str(category.id)})
        )
        return format_html(
            "<a href='{}'>{}</a>", url, category.commodities_count
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(commodities_count=Count("commodity"))
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

    @admin.display(ordering="market_count")
    def market_count(self, contact_person):
        url = (
            reverse("admin:mktdirectory_market_changelist")
            + "?"
            + urlencode({"contact_person_id": str(contact_person.id)})
        )
        return format_html(
            "<a href='{}'>{}</a>", url, contact_person.market_count
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(market_count=Count("market"))
        )
