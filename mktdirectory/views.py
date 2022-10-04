from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from mktdirectory.models import Commodity, Market
from mktdirectory.serializers import CommoditySerializer, MarketSerializer


@api_view(["GET", "POST"])
def commodity_list(request):
    """
    List all commodities
    """
    if request.method == "GET":
        commodities = Commodity.objects.select_related("category").all()
        serializer = CommoditySerializer(commodities, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        """create a commodity"""
        serializer = CommoditySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def commodity_detail(request, pk):

    commodity = get_object_or_404(Commodity, pk=pk)
    if request.method == "GET":
        serializer = CommoditySerializer(commodity)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CommoditySerializer(commodity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        commodity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
