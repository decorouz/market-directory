from rest_framework import serializers
from .models import Market


class MarketDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = (
            "market_code",
            "name",
            "brief_details",
            "num_vendors",
            "market_schedule",
            "reference_mkt_date",
        )
