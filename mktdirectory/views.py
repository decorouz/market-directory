from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Count

from mktdirectory.models import Category, Commodity, Market
from mktdirectory.serializers import (
    CommoditySerializer,
    MarketSerializer,
    CategorySerializer,
)


class CategoryList(APIView):
    def get(self, request):
        query_set = Category.objects.annotate(
            commodities_count=Count("commodity")
        ).all()
        serializer = CategorySerializer(
            query_set, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    def get_object(self, pk):
        query_set = Category.objects.annotate(
            commodities_count=Count("commodity")
        )
        return get_object_or_404(query_set, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category.commodity_set.count() > 0:
            return Response(
                {
                    "error": "Category can not be deleted because it is associated with one or more Commodity"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


@api_view(["GET", "PATCH", "DELETE"])
def commodity_detail(request, pk):

    commodity = get_object_or_404(Commodity, pk=pk)
    if request.method == "GET":
        serializer = CommoditySerializer(commodity)
        return Response(serializer.data)
    elif request.method == "PATCH":
        serializer = CommoditySerializer(commodity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        commodity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def market_list(request):
    """List all markets"""
    if request.method == "GET":
        query_set = (
            Market.objects.select_related("contact_person")
            .all()
            .prefetch_related("commodities")
        )
        serializers = MarketSerializer(query_set, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = MarketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view()
def market_detail(request, pk):
    market = get_object_or_404(Market, pk=pk)
    serializers = MarketSerializer(market)
    return Response(serializers.data)
