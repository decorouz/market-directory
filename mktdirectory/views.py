from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count

from mktdirectory.models import Category, Commodity, Market
from mktdirectory.serializers import (
    CommoditySerializer,
    MarketSerializer,
    CategorySerializer,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        commodities_count=Count("commodity")
    ).all()

    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, pk):
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


class CommodityViewSet(ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer


class MarketViewSet(ModelViewSet):
    queryset = (
        Market.objects.select_related("contact_person")
        .all()
        .prefetch_related("commodities", "accepted_payment_types")
    )

    serializer_class = MarketSerializer
