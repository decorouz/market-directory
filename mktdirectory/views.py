from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from mktdirectory.models import Commodity, Market, MarketDay
from mktdirectory.serializers import CommoditySerializer, MarketSerializer


@api_view()
def commodity_list(request):
    """
    List all commodities
    """
    commodities = Commodity.objects.select_related("category").all()
    serializer = CommoditySerializer(commodities, many=True)
    return Response(serializer.data)


@api_view()
def commodity_detail(request, pk):
    commodity = get_object_or_404(Commodity, pk=pk)
    serializer = CommoditySerializer(commodity)
    return Response(serializer.data)


@api_view()
def market_list(request):
    """List all markets"""

    markets = (
        Market.objects.select_related("contact_person")
        .all()
        .prefetch_related("commodities")
    )
    serializers = MarketSerializer(markets, many=True)
    return Response(serializers.data)


@api_view()
def market_detail(request, pk):
    market = get_object_or_404(Market, pk=pk)
    serializers = MarketSerializer(market)
    return Response(serializers.data)
