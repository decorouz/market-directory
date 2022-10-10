from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.db.models import Count

from mktdirectory.models import Category, Commodity, Market, Review
from mktdirectory.serializers import (
    CommoditySerializer,
    MarketSerializer,
    CategorySerializer,
    ReviewSerializer,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        commodities_count=Count("commodity")
    ).all()

    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if Commodity.objects.filter(category_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Category can not be deleted because it is associated with one or more Commodity"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CommodityViewSet(ModelViewSet):

    serializer_class = CommoditySerializer

    def get_queryset(self):
        queryset = Commodity.objects.all()
        category_id = self.request.query_params.get("category_id")
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class MarketViewSet(ModelViewSet):
    # To-do
    #Filter by market date
    #Filter by contact person
    # Filter by commodities
    # Filter by location(state, Lga, two)
    # Filter by payment methods

    queryset = Market.objects.select_related(
        "contact_person"
    ).prefetch_related("commodities", "accepted_payment_types")

    serializer_class = MarketSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(market_id=self.kwargs["market_pk"])

    # Goto Serializer create method
    def get_serializer_context(self):
        return {"market_id": self.kwargs["market_pk"]}
