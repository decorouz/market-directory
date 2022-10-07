from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count

from mktdirectory.models import Category, Commodity, Market
from mktdirectory.serializers import (
    CommoditySerializer,
    MarketSerializer,
    CategorySerializer,
)


class CategoryList(ListCreateAPIView):
    def get_queryset(self):
        return Category.objects.annotate(
            commodities_count=Count("commodity")
        ).all()

    def get_serializer_class(self):
        return CategorySerializer

    def get_serializer_context(self):
        return {"request": self.request}


# Category View
class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if category.commodity_set.count() > 0:
            return Response(
                {
                    "error": "Category can not be deleted because it is associated with one or more Commodity"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommodityList(ListCreateAPIView):
    def get_queryset(self):
        return Commodity.objects.select_related("category").all()

    def get_serializer_class(self):
        return CommoditySerializer


# Commodity Views
class CommodityDetail(RetrieveUpdateDestroyAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer


class MarketList(ListCreateAPIView):
    def get_queryset(self):
        query_set = (
            Market.objects.select_related("contact_person")
            .all()
            .prefetch_related("commodities", "accepted_payment_types")
        )
        return query_set

    def get_serializer_class(self):
        return MarketSerializer


class MarketDetail(RetrieveUpdateDestroyAPIView):
    queryset = (
        Market.objects.select_related("contact_person")
        .all()
        .prefetch_related("commodities")
    )
    serializer_class = MarketSerializer
