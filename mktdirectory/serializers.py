from dataclasses import fields
from rest_framework import serializers

from mktdirectory.models import (
    AcceptedPaymentMethod,
    Commodity,
    ContactPerson,
    Market,
    Category,
    MarketDay,
)
from datetime import timedelta, date


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "commodities_count")

    commodities_count = serializers.IntegerField(read_only=True)


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ("id", "name", "grade", "category", "overview")
        


class ContactPersonSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name="get_fullname")

    class Meta:
        model = ContactPerson
        fields = ("full_name", "phone", "email")

    def get_fullname(self, contact_person: ContactPerson):
        return f"{contact_person.first_name} {contact_person.last_name}"


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedPaymentMethod
        fields = ("type", "charges")


class MarketDaySerializer(serializers.ModelSerializer):
    # name = serializers.SerializerMethodField(method_name="get_commodity_name")

    class Meta:

        model = MarketDay
        fields = (
            "commodity",
            "grade",
            "commodity_price",
        )


class SimpleCommoditySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="get_name")

    class Meta:
        model = Commodity
        fields = ("name",)

    def get_name(self, obj: Commodity):
        if obj.grade:
            return f"{obj.grade}-{obj.name}"
        return f"{obj.name}"


class MarketSerializer(serializers.ModelSerializer):
    contact_person = ContactPersonSerializer()
    # accepted_payment_types = PaymentTypeSerializer(many=True)
    schedule_in_days = serializers.IntegerField(source="market_days_interval")
    market_site = serializers.CharField(source="location_description")
    next_market_day = serializers.SerializerMethodField(
        method_name="calculate_next_marketdate"
    )
    commodities = SimpleCommoditySerializer(many=True)

    class Meta:
        model = Market
        fields = (
            "market_code",
            "name",
            "brief_details",
            "market_site",
            "schedule_in_days",
            "num_vendors",
            "next_market_day",
            "contact_person",
            "last_update",
            "commodities",
        )

    def calculate_next_marketdate(self, market: Market):
        """Calculate the next market day"""
        today = date.today()
        ref_date = market.reference_mkt_date
        interval = timedelta(market.market_days_interval)

        while ref_date <= today:
            ref_date = ref_date + interval
        return ref_date
