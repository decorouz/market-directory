from django_filters.rest_framework import FilterSet
from .models import Market


# To-do
# filter by:
# commodities, location(state, lga, two), payment methods, commodities, accepted_payment method.
#
class MarketFilter(FilterSet):
    class Meta:
        model = Market
        fields = {
            "market_days_interval": ["exact"],
            "contact_person": ["exact"],
        }
