from django.contrib import admin
from .models import (
    Commodity,
    Category,
    ContactPerson,
    Market,
    AcceptedPaymentMethod,
    MarketDay,
)


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ["name", "overview"]
    list_per_page: int = 10


@admin.register(ContactPerson)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone")
    list_per_page = 10


@admin.register(AcceptedPaymentMethod)
class AcceptablePaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("type", "charges")
    list_editable = ("charges",)


admin.site.register(Market)
admin.site.register(MarketDay)


admin.site.register(Category)
