from rest_framework import serializers
from django.db.models import Count
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    AcceptedPaymentMethod,
    Commodity,
    ContactPerson,
    Market,
    Category,
    MarketCommodity,
    Review,
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


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ("id", "name", "grade", "category", "overview")

        validators = [
            UniqueTogetherValidator(queryset=Commodity.objects.all(), fields=["name", "grade"])
        ]

    # get the price of the commodity at the previous market day.


class MarketInstanceSerializer(serializers.ModelSerializer):
    class Meta:

        model = MarketCommodity
        fields = ("id", "commodity")


class MarketSerializer(serializers.ModelSerializer):
    schedule_in_days = serializers.IntegerField(source="market_days_interval")
    market_site = serializers.CharField(source="location_description")
    next_market_day = serializers.SerializerMethodField(method_name="calculate_next_marketdate")

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
            "accepted_payment_types",
        )
        depth = 1

    def calculate_next_marketdate(self, market: Market):
        """Calculate the next market day"""
        today = date.today()
        ref_date = market.reference_mkt_date
        interval = timedelta(market.market_days_interval)

        while ref_date <= today:
            ref_date = ref_date + interval
        return ref_date

    # get price of commodity at previous market day

    def get_recent_commodity_price(self, commodity, market):
        """Get the previous commodity price at a market"""
        pass


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "date", "name", "description")

    def create(self, validated_data):
        market_id = self.context["market_id"]
        return Review.objects.create(market_id=market_id, **validated_data)
