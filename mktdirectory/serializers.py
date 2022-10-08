from rest_framework import serializers
from django.db.models import Count
from rest_framework.validators import UniqueTogetherValidator

from mktdirectory.models import (
    AcceptedPaymentMethod,
    Commodity,
    ContactPerson,
    Market,
    Category,
    MarketDay,
)
from datetime import timedelta, date


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = ("first_name", "last_name", "phone", "email")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description", "commodities_count")

    commodities_count = serializers.IntegerField(read_only=True)


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


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ("id", "name", "grade", "category", "overview")

        validators = [
            UniqueTogetherValidator(
                queryset=Commodity.objects.all(), fields=["name", "grade"]
            )
        ]


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
    schedule_in_days = serializers.IntegerField(source="market_days_interval")
    market_site = serializers.CharField(source="location_description")
    next_market_day = serializers.SerializerMethodField(
        method_name="calculate_next_marketdate"
    )

    class Meta:
        model = Market
        fields = (
            "market_code",
            "name",
            "brief_detail",
            "market_site",
            "schedule_in_days",
            "num_vendor",
            "next_market_day",
            "contact_person",
            "reference_mkt_date",
            "commodities",
            "accepted_payment_types",
        )

    def calculate_next_marketdate(self, market: Market):
        """Calculate the next market day"""
        today = date.today()
        ref_date = market.reference_mkt_date
        interval = timedelta(market.market_days_interval)

        while ref_date <= today:
            ref_date = ref_date + interval
        return ref_date
